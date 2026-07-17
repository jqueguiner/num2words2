//! Presentation / dispatch helpers ported from `num2words2/__init__.py`.
//!
//! These three functions were the last pieces of pure-Python logic living in
//! the `num2words2` binder: language-code resolution, the `style=`
//! post-processing, and the `cents=` mode mapping. They are conversion-agnostic
//! string/enum transforms, so they belong in the pure core rather than the
//! Python surface. The PyO3 binder classifies the caller's arguments into the
//! plain types below and calls these directly.

/// Resolve a caller's language code to a core key, mirroring the historic
/// dispatcher (`num2words2.__init__._normalize_lang`):
///
/// 1. exact match, then
/// 2. hyphen -> underscore, then
/// 3. `xx_YY` casing, then
/// 4. the bare two-letter prefix.
///
/// Returns `None` when none match; the binder turns that into the same empty
/// `NotImplementedError` the Python raised.
pub fn resolve_lang(raw: &str) -> Option<String> {
    let keys = crate::supported_lang_keys();
    // `keys.contains(&s)` cannot be used: the keys are `&'static str` and the
    // needle is a borrowed `&str`, so the slice `contains` type-checks fail.
    #[allow(clippy::manual_contains)]
    let known = |s: &str| keys.iter().any(|k| *k == s);

    if known(raw) {
        return Some(raw.to_string());
    }
    let nl = raw.replace('-', "_");
    if known(&nl) {
        return Some(nl);
    }
    let parts: Vec<&str> = nl.split('_').collect();
    if parts.len() >= 2 {
        let candidate = format!("{}_{}", parts[0].to_lowercase(), parts[1].to_uppercase());
        if known(&candidate) {
            return Some(candidate);
        }
        if known(parts[0]) {
            return Some(parts[0].to_string());
        }
    }
    let prefix: String = nl.chars().take(2).collect();
    if known(&prefix) {
        return Some(prefix);
    }
    None
}

/// `style=` presentation post-processing (issues #535, #562), mirroring
/// `num2words2.__init__._apply_style`. Operates on the rendered string, so it
/// is conversion-independent:
///
/// * `style="terse"` + `to == "ordinal"` strips a leading `"one "`/`"un "`/
///   `"uno "` (but never reduces the whole string to empty).
/// * `style="us"` + an English `lang` replaces `" and "` with `" "`.
pub fn apply_style(result: &str, style: Option<&str>, to: &str, lang: &str) -> String {
    let mut out = result.to_string();
    if style == Some("terse") && to == "ordinal" {
        for prefix in ["one ", "un ", "uno "] {
            if out.starts_with(prefix) && out.len() > prefix.len() {
                out = out[prefix.len()..].to_string();
                break;
            }
        }
    }
    if style == Some("us") && lang.starts_with("en") {
        out = out.replace(" and ", " ");
    }
    out
}

/// The `cents=` argument as the binder classifies the caller's Python object.
pub enum CentsArg<'a> {
    /// The kwarg was not supplied at all (Python default `True`).
    Absent,
    /// A real Python `bool`.
    Bool(bool),
    /// A Python `str` (only the three keywords are meaningful).
    Str(&'a str),
    /// Any other type — Python keeps it as-is, and the caller's
    /// `_cents in (True, False)` guard then rejects it.
    Other,
}

/// `cents='omit'|'verbose'|'terse'` -> the legacy bool the core expects
/// (issue #554), mirroring `num2words2.__init__._normalize_cents` **plus** the
/// caller's follow-up `_cents in (True, False)` guard.
///
/// Returns `Some((cents_bool, drop_cents))` when the value resolves to a usable
/// bool (absent, a real bool, or one of the three keywords); `drop_cents` means
/// the value should be truncated to an int so no cents segment appears.
/// Returns `None` when Python would have kept a non-bool value and the guard
/// would reject it (the binder then declines the call).
pub fn normalize_cents(cents: CentsArg) -> Option<(bool, bool)> {
    match cents {
        CentsArg::Absent => Some((true, false)),
        CentsArg::Str("omit") => Some((true, true)),
        CentsArg::Str("verbose") => Some((true, false)),
        CentsArg::Str("terse") => Some((false, false)),
        CentsArg::Bool(b) => Some((b, false)),
        CentsArg::Str(_) | CentsArg::Other => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resolve_exact_and_hyphen() {
        assert_eq!(resolve_lang("en").as_deref(), Some("en"));
        assert_eq!(resolve_lang("pt_BR").as_deref(), Some("pt_BR"));
        // hyphen -> underscore, exact key
        assert_eq!(resolve_lang("pt-BR").as_deref(), Some("pt_BR"));
    }

    #[test]
    fn resolve_casing_and_prefix() {
        // en-US: no en_US key, casing candidate missing, prefix "en" wins.
        assert_eq!(resolve_lang("en-US").as_deref(), Some("en"));
        assert_eq!(resolve_lang("en_US").as_deref(), Some("en"));
        // Two-letter-prefix fallback on a longer word.
        assert_eq!(resolve_lang("english").as_deref(), Some("en"));
    }

    #[test]
    fn resolve_unknown() {
        assert_eq!(resolve_lang("unknown_lang"), None);
        assert_eq!(resolve_lang("zz"), None);
    }

    #[test]
    fn style_terse_strips_leading_one() {
        assert_eq!(
            apply_style("one hundredth", Some("terse"), "ordinal", "en"),
            "hundredth"
        );
        // Exactly "first" is untouched (no leading "one ").
        assert_eq!(apply_style("first", Some("terse"), "ordinal", "en"), "first");
        // terse only applies to ordinal.
        assert_eq!(
            apply_style("one hundred", Some("terse"), "cardinal", "en"),
            "one hundred"
        );
    }

    #[test]
    fn style_us_drops_and() {
        assert_eq!(
            apply_style("one thousand and one", Some("us"), "cardinal", "en"),
            "one thousand one"
        );
        // Non-English lang is untouched.
        assert_eq!(
            apply_style("mil y uno", Some("us"), "cardinal", "es"),
            "mil y uno"
        );
        // No style is a no-op.
        assert_eq!(apply_style("x and y", None, "cardinal", "en"), "x and y");
    }

    #[test]
    fn cents_modes() {
        assert_eq!(normalize_cents(CentsArg::Absent), Some((true, false)));
        assert_eq!(normalize_cents(CentsArg::Str("omit")), Some((true, true)));
        assert_eq!(normalize_cents(CentsArg::Str("verbose")), Some((true, false)));
        assert_eq!(normalize_cents(CentsArg::Str("terse")), Some((false, false)));
        assert_eq!(normalize_cents(CentsArg::Bool(true)), Some((true, false)));
        assert_eq!(normalize_cents(CentsArg::Bool(false)), Some((false, false)));
        assert_eq!(normalize_cents(CentsArg::Str("nope")), None);
        assert_eq!(normalize_cents(CentsArg::Other), None);
    }
}

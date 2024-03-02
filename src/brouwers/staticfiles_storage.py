from django.contrib.staticfiles import storage


class ManifestStaticFilesStorage(storage.ManifestStaticFilesStorage):
    manifest_strict = False  # otherwise breaks on missing vendor sourcemaps
    patterns = (
        (
            "*.css",
            (
                r"""(?P<matched>url\(['"]{0,1}\s*(?P<url>.*?)["']{0,1}\))""",
                (
                    r"""(?P<matched>@import\s*["']\s*(?P<url>.*?)["'])""",
                    """@import url("%(url)s")""",
                ),
                # (
                #     (
                #         r"(?m)(?P<matched>)^(/\*#[ \t]"
                #         r"(?-i:sourceMappingURL)=(?P<url>.*)[ \t]*\*/)$"
                #     ),
                #     "/*# sourceMappingURL=%(url)s */",
                # ),
            ),
        ),
        # (
        #     "*.js",
        #     (
        #         (
        #             r"(?m)(?P<matched>)^(//# (?-i:sourceMappingURL)=(?P<url>.*))$",
        #             "//# sourceMappingURL=%(url)s",
        #         ),
        #     ),
        # ),
    )

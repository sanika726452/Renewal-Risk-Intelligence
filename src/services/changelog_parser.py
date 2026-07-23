import re


class ChangelogParser:

    def __init__(self):

        self.deprecated_sdks = []
        self.deprecated_features = []
        self.new_features = []
        self.migration_required = False
        self.summary = ""

    def parse(self, changelog_text):

        lines = changelog_text.split("\n")

        for line in lines:

            line = line.strip()

            if len(line) == 0:
                continue

            lower = line.lower()

            # ------------------------------------
            # Deprecated SDK Versions
            # ------------------------------------

            sdk_match = re.findall(r"v\d+\.\d+", line)

            if "deprecated" in lower or "sunset" in lower:

                for sdk in sdk_match:

                    if sdk not in self.deprecated_sdks:
                        self.deprecated_sdks.append(sdk)

                self.deprecated_features.append(line)

            # ------------------------------------
            # Migration Required
            # ------------------------------------

            if "migrate" in lower or "migration" in lower:

                self.migration_required = True

            # ------------------------------------
            # New Features
            # ------------------------------------

            if line.startswith("-"):

                feature = line.replace("-", "").strip()

                self.new_features.append(feature)

        self.summary = self.generate_summary()

        return {
            "deprecated_sdks": self.deprecated_sdks,
            "deprecated_features": self.deprecated_features,
            "new_features": self.new_features,
            "migration_required": self.migration_required,
            "summary": self.summary
        }

    def generate_summary(self):

        text = ""

        if len(self.deprecated_sdks) > 0:

            text += (
                "Deprecated SDKs detected: "
                + ", ".join(self.deprecated_sdks)
                + ". "
            )

        if self.migration_required:

            text += (
                "Customers should migrate to newer SDK versions. "
            )

        if len(self.deprecated_features) > 0:

            text += (
                f"{len(self.deprecated_features)} deprecated "
                "product changes detected."
            )

        return text
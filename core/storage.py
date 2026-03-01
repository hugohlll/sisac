from whitenoise.storage import CompressedManifestStaticFilesStorage
import pathlib

class CustomWhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def _compress_path(self, full_path, **kwargs):
        """
        Gracefully handle missing files during Django 5 collection.
        Some third-party packages or Django admin might reference files that 
        don't exist in the staticfiles dir, causing compression to crash.
        """
        if not pathlib.Path(full_path).exists():
            return []
        
        try:
            # Yield from the parent generator securely
            for compressed in super()._compress_path(full_path, **kwargs):
                yield compressed
        except FileNotFoundError:
            pass

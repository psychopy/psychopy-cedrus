from psychopy.tests.utils import profiledImport


def test_component_import():
    """
    Test that Components can be imported in good time and without touching costly packages.
    """
    for ref in [
        "psychopy_cedrus.components.lumina",
        "psychopy_cedrus.components.rb",
        "psychopy_cedrus.components.riponda",
        "psychopy_cedrus.components.stimtracker",
    ]:
        profiledImport(
            ref=ref,
            notouch=[
                "psychopy.hardware",
                "pyxid2",
                "psychopy_cedrus.lumina",
                "psychopy_cedrus.rb",
                "psychopy_cedrus.riponda",
                "psychopy_cedrus.stimtracker",
            ]
        )

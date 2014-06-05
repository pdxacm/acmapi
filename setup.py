import setuptools

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement
# object
install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

if __name__ == "__main__":
    setuptools.setup(
        name="acmapi",
        version="0.2.0",
        description="",
        author="Cameron Brandon White",
        author_email="cameronbwhite90@gmail.com",
        url="https://github.com/cameronbwhite/acmapi",
        packages = [
            'acmapi',
        ],
        install_requires = reqs,
        test_requires = [
            "Nose",
            "Mock",
            "FreezeGun",
        ],
        include_package_data=True,
        zip_safe=False,
    )

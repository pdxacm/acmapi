import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="acmapi",
        version="0.1.0",
        description="",
        author="Cameron Brandon White",
        author_email="cameronbwhite90@gmail.com",
        url="https://github.com/cameronbwhite/acmapi",
        install_requires = [
            "Flask",
            "Flask-SQLAlchemy",
            "Flask-RESTful",
        ],
        test_requires = [
            "Nose",
            "Mock",
            "FreezeGun",
        ],
        include_package_data=True,
        zip_safe=False,
    )

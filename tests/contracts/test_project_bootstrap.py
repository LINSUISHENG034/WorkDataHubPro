def test_project_package_exposes_version() -> None:
    import work_data_hub_pro

    assert work_data_hub_pro.__version__ == "0.1.0"

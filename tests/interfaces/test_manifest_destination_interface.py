from interfaces.manifest_destination_interface import ManifestDestinationInterface, SamePrefixDestinationInterface


class TestSamePrefixDestinationInterface:
    def test_same_prefix_destination_interface_returns_same_bucket(self):
        # arrange
        destination = SamePrefixDestinationInterface()

        # act
        bucket, _ = destination.get(
            source_bucket="my-bucket",
            source_key="datasets/mydata/file.csv"
        )

        # assert
        assert bucket == "my-bucket"

    def test_same_prefix_destination_interface_appends_mani_extension(self):
        # arrange
        destination = SamePrefixDestinationInterface()

        # act
        bucket, _ = destination.get(
            source_bucket="my-bucket",
            source_key="datasets/mydata/file.csv"
        )

        # assert
        assert bucket == "my-bucket"


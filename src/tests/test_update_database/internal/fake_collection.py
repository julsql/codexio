from test_update_database.internal.fake_profile import FakeProfile


class FakeCollection:
    def __init__(self, id, profile_name="BD"):
        self.id = id
        self.profile = FakeProfile(profile_name)
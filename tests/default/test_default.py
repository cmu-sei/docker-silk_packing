def test_silk_version(host):
    version = "3.23.1"
    command = """/netsa/bin/silk_config --silk-version"""

    cmd = host.run(command)

    assert version in cmd.stdout

from unittest.mock import (
    patch, call, Mock
)
from pytest import raises

from suse_migration_services.units.grub_setup import main
from suse_migration_services.exceptions import (
    DistMigrationGrubConfigException
)


class TestSetupHostNetwork(object):
    @patch('suse_migration_services.command.Command.run')
    def test_main_raises_on_grub_update(
        self, mock_Command_run
    ):
        mock_Command_run.side_effect = Exception
        with raises(DistMigrationGrubConfigException):
            main()

    @patch('suse_migration_services.command.Command.run')
    @patch('suse_migration_services.units.grub_setup.Fstab')
    def test_main(
            self, mock_Fstab, mock_Command_run
    ):
        fstab = Mock()
        mock_Fstab.return_value = fstab
        main()
        fstab.read.assert_called_once_with(
            '/etc/system-root.fstab'
        )
        assert mock_Command_run.call_args_list == [
            call(
                [
                    'mount', '--bind', '/dev',
                    '/system-root/dev'
                ]
            ),
            call(
                [
                    'mount', '--bind', '/proc',
                    '/system-root/proc'
                ]
            ),
            call(
                [
                    'chroot', '/system-root',
                    'grub2-mkconfig', '-o', '/boot/grub2/grub.cfg'
                ]
            )
        ]

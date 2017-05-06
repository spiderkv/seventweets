import abc

class Migration(metaclass=abc.ABCMeta):
    """
    Base class for all migrations. It is used to define common interface for
    all migrations that `MigrationManager` knows how to use and as a way to
    discover all migrations (all subclasses of this class).
    """

    @abc.abstractmethod
    def id(self):
        """
        All migrations have to have unique ID. This methods returns it.
        IDs have to be integers and IDs have to be incremented in comparison
        to previous migrations since this ID is used to determine which
        migrations are applied and which are not.
        """
        pass

    @abc.abstractmethod
    def upgrade(self, cursor):
        """
        Performs operations on database to upgrade current schema.
        :param cursor: Database cursor.
        """
        pass

    @abc.abstractmethod
    def downgrade(self, cursor):
        """
        Performs operations on database to downgrade current schema.
        :param cursor: Database cursor.
        """
        pass
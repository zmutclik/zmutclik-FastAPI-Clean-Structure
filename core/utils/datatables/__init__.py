"""Sqlalchemy2-datatables library, provides serverside implementation for jQuery Datatables"""

__version__ = '0.6.2'

from .base import DTDataCallbacks
from .datatable import DataTable

__all__ = ['DataTable', 'DTDataCallbacks']

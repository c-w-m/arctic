===============================================================================
=============================== warnings summary ===============================

tests/integration/test_arctic.py::test_list_libraries_cached
  /home/travis/build/man-group/arctic/tests/integration/test_arctic.py:250: DeprecationWarning: remove is deprecated. Use delete_one or delete_many instead.
    arctic._conn.meta_db.cache.remove({})

tests/integration/chunkstore/test_chunkstore.py::test_write_dataframe_with_func
  /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/pandas/core/indexing.py:621: SettingWithCopyWarning: 
  A value is trying to be set on a copy of a slice from a DataFrame.
  Try using .loc[row_indexer,col_indexer] = value instead
  
  See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    self.obj[item_labels[indexer[info_axis]]] = value

tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size0]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size1]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size2]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size3]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size4]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size5]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size6]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size7]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size8]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size9]
  /home/travis/build/man-group/arctic/tests/integration/store/test_pandas_store.py:652: DeprecationWarning: 
  Panel is deprecated and will be removed in a future version.
  The recommended way to represent these types of 3-dimensional data are with a MultiIndex on a DataFrame, via the Panel.to_frame() method
  Alternatively, you can use the xarray package http://xarray.pydata.org/en/stable/.
  Pandas provides a `.to_xarray()` method to help automate this conversion.
  
    pn = panel(*df_size)

tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size0]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size1]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size2]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size3]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size4]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size5]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size6]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size7]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size8]
tests/integration/store/test_pandas_store.py::test_panel_save_read[df_size9]
  /home/travis/build/man-group/arctic/arctic/store/_pandas_ndarray_store.py:245: DeprecationWarning: 
  Panel is deprecated and will be removed in a future version.
  The recommended way to represent these types of 3-dimensional data are with a MultiIndex on a DataFrame, via the Panel.to_frame() method
  Alternatively, you can use the xarray package http://xarray.pydata.org/en/stable/.
  Pandas provides a `.to_xarray()` method to help automate this conversion.
  
    return item.iloc[:, 0].unstack().to_panel()

tests/integration/store/test_pandas_store.py::test_panel_save_read_with_nans
  /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/_pytest/python.py:174: DeprecationWarning: 
  Panel is deprecated and will be removed in a future version.
  The recommended way to represent these types of 3-dimensional data are with a MultiIndex on a DataFrame, via the Panel.to_frame() method
  Alternatively, you can use the xarray package http://xarray.pydata.org/en/stable/.
  Pandas provides a `.to_xarray()` method to help automate this conversion.
  
    testfunction(**testargs)

tests/integration/store/test_pandas_store.py::test_panel_save_read_with_nans
  /home/travis/build/man-group/arctic/arctic/store/_pandas_ndarray_store.py:246: DeprecationWarning: 
  Panel is deprecated and will be removed in a future version.
  The recommended way to represent these types of 3-dimensional data are with a MultiIndex on a DataFrame, via the Panel.to_frame() method
  Alternatively, you can use the xarray package http://xarray.pydata.org/en/stable/.
  Pandas provides a `.to_xarray()` method to help automate this conversion.
  
    return item.to_panel()

tests/integration/store/test_pandas_store.py::test_duplicate_labels
tests/integration/store/test_pandas_store.py::test_duplicate_labels
tests/integration/store/test_pandas_store.py::test_duplicate_labels
tests/integration/store/test_pandas_store.py::test_duplicate_labels
tests/integration/store/test_pandas_store.py::test_duplicate_labels
tests/integration/store/test_pandas_store.py::test_duplicate_labels
  /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/numpy/core/numeric.py:2591: DeprecationWarning: elementwise comparison failed; this will raise an error in the future.
    return bool(asarray(a1 == a2).all())

tests/integration/tickstore/test_toplevel.py::test_should_return_data_when_date_range_falls_in_a_single_underlying_library
  /home/travis/build/man-group/arctic/arctic/tickstore/tickstore.py:419: FutureWarning: Conversion of the second argument of issubdtype from `int` to `np.signedinteger` is deprecated. In future, it will be treated as `np.int64 == np.dtype(int).type`.
    if np.issubdtype(dtype, int):

===============================================================================

1317 passed, 
   3 skipped
   6 xfailed
  13 xpassed
  41 warnings in
1375.97 seconds

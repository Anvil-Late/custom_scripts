def combine_low_occurences(vector, thresh=0.01, return_combined_bin_value=False):
    """Combines low frequency values of a categorical variable.

    This function takes as input a vector, a threshold and a new bin value.
    All values that have a frequency below the threshold will be combined into
    a new category named after the new bin value

    ---
    Parameters:
    - vector : pd.Series, categorical vector on which the function is applied
    - thresh : Threshold below which a value is considered of low frequency.
      Can either be int >= 1 for counts or float < 1 for proportions.
      Default : 0.1
    - return_combined_bin_value : Bool, whether the function returns the bin value
      of the converted values. Default : False
    ---
    Returns a pd.Series
    """
    if thresh < 1:
        thresh_kind = "prop"
    else:
        if type(thresh) is int:
            thresh_kind = "count"
        else:
            raise TypeError("'thresh' parameter must either be int or float < 1")

    if thresh_kind == "prop":
        occurence_table = vector.value_counts(normalize=True)
    else:
        occurence_table = vector.value_counts(normalize=False)

    # Converting low occurence bins
    bin_conversion_table = {}
    for bin_name, bin_occurence in occurence_table.iteritems():
        if bin_occurence < thresh:
            bin_conversion_table[bin_name] = np.inf
        else:
            bin_conversion_table[bin_name] = bin_name

    converted_vector = vector.map(lambda X: bin_conversion_table[X])

    # renaming the bins for continuity
    all_bins = np.sort(converted_vector.unique()).tolist()
    bin_rename_dict = {}
    for idx, bin_nr in enumerate(all_bins):
        bin_rename_dict[bin_nr] = idx + 1

    if return_combined_bin_value:
        return converted_vector.map(lambda X: bin_rename_dict[X]), bin_rename_dict[np.inf]
    return converted_vector.map(lambda X: bin_rename_dict[X])
  
def rename_multiindex_columns(df):
  """
  Function that concatenates multiple levels of column names into a single level

  Parameters
  ----------
  df : pd.DataFrame
      dataframe whose multiindex columns need to be renamed

  Returns
  -------
  pandas.core.indexes.base.Index : single-leveled column names

  """
  return df.columns.map('_'.join).str.strip('_')

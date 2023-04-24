import pandas as pd

class Test:
    def is_equal(a,b) -> bool:
        return a == b
    
    def is_dataframe_equal(a:pd.DataFrame,b:pd.DataFrame) -> bool:
        return a.equals(b)
    
    def get_number_tiles_in_dash(dash):
        return len(dash.dashboard_elements)
    
    def get_number_filters_in_dash(dash):
        return len(dash.dashboard_filters)
    
    def get_hash_of_all_filters(dash):
        return hash(frozenset([str(val) for val in sorted(dash.dashboard_filters, key= lambda obj: obj.id)]))

    def get_type_of_dashboard(dash):
        # UDD - User defined dashboard
        return 'LookML Dashboard' if dash.lookml_link_id else 'UDD'
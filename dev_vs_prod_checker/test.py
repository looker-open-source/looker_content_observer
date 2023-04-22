import pandas as pd

class Test:
    def __init__(self) -> None:
        pass

    def is_equal(self,a,b) -> bool:
        return a == b
    
    def is_dataframe_equal(self,a:pd.DataFrame,b:pd.DataFrame) -> bool:
        return a.equals(b)
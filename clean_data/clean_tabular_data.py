'''
Cleaning the tabular dataset.
@author:    Behzad 
@date:      10 September 2022
'''
import pandas as pd
import re

pd.set_option('display.max_columns', None)
class CleanData:

    '''
    This class will clean text data and has the following methods:

    csv_to_df(self)
    clean_text_data(self)
    '''

    def csv_to_df(self):

        '''
        Opens csv file in a DataFrame and pre-cleans the data

        RETURNS
        -------
        DataFrame
            A pre cleaned DataFrame
        '''
        self.path = "/Users/behzad/AiCore/Facebook_Marketplace_RRS/ml_models/"
        df = pd.read_csv(self.path + "Products.csv", lineterminator="\n")
        df = df.drop(df.columns[[0]], axis=1)
        df['price'] = df['price'].str.replace('£', '')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df_pre_clean = df[df.location.notnull()].reset_index() # Only 'price' has null values
        #print(df_pre_clean.columns)
        #print(df_pre_clean.head(10))
        return df_pre_clean

    def clean_text_data(self, csv_save: bool = False, pkl_save: bool = False):

        '''
        Cleans data by removing not usful data from each column
        '''
        df = self.csv_to_df()
        df_tmp_name = df.join(df['product_name'].str.split('|', 0, expand=True).rename(columns={0:'product_name_edited'}))
        df_tmp_ctg = df['category'].str.split('/', expand=True)
        df_tmp_ctg = df_tmp_ctg.rename(columns={0:'category_edited', 1:'category_description'})
        df_tmp_ctg['category_description_edited'] = df_tmp_ctg[df_tmp_ctg.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
        df_ctg = df_tmp_ctg.filter(['category_edited', 'category_description_edited'])
        df_tmp = pd.concat([df_tmp_name, df_ctg], axis=1)
        df_clean = df_tmp.filter(['id', 'product_name_edited', 'category_edited', 'category_description_edited', 'product_description', 'price', 'location'])
        df_clean['product_name_edited'] = df_clean['product_name_edited'].str.replace('[^a-zA-Z]', ' ')
        # df_clean['category_edited'] = df_clean['category_edited'].str.replace('[^a-zA-Z]', ' ')
        df_clean['category_description_edited'] = df_clean['category_description_edited'].str.replace('[^a-zA-Z]', ' ')
        df_clean['product_description'] = df_clean['product_description'].str.replace('[^a-zA-Z]', ' ')
        df_clean['product_description'] = df_clean['product_description'].map(lambda x: ' '.join(word for word in x.split() if len(word)>1))
        df_clean['location'] = df_clean['location'].str.replace('[^a-zA-Z]', ' ')
        if csv_save:
            df_clean.to_csv(self.path + 'products_clean.csv', index = None, header=True)
        #print(df_clean.head(10))

        df_img = pd.read_csv(self.path + "Images.csv")
        df_merge = pd.merge(df_clean, df_img[['product_id', 'id']], left_on='id', right_on='product_id').copy()
        df_merge = df_merge.drop(df_merge.columns[[0,7]], axis=1)
        df_merge = df_merge.rename(columns={'id_y':'id'})
        if pkl_save:
           df_merge.to_csv(self.path + 'products_image_merged.csv', index = None, header=True)
        #print(df_merge.tail())
        return df_merge

if __name__ == '__main__':
    cln = CleanData() 
    #cln.clean_text_data(True)
    cln.clean_text_data(True, True)
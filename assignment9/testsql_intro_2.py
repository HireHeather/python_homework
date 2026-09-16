import os   
import sqlite3
import pandas as pd
import warnings


warnings.simplefilter(action="ignore", category=FutureWarning)


LESSON_DB_PATH = os.path.join("..", "db", "lesson.db")



def main():
   
    print(f"Connecting to lesson database asset at: {LESSON_DB_PATH}")

   
    # STEP 3: ESTABLISHING SAFE DATABASE CONNECTIONS
   
    try:
       
        conn = sqlite3.connect(LESSON_DB_PATH)

  
        # STEP 4: WRITING THE SQL RELATIONAL JOIN COMMAND
        
     
        query = """
            SELECT 
                line_items.line_item_id, 
                line_items.quantity, 
                line_items.product_id, 
                products.product_name, 
                products.price 
            FROM line_items
            INNER JOIN products ON line_items.product_id = products.product_id;
        """

        print("\nLoading SQL tracking metrics into a Pandas DataFrame...")
        
        
        df = pd.read_sql_query(query, conn).copy()

       
        print("\n--- Initial Raw Joined Data Frame Snapshot (First 5 Rows) ---")
        print(df.head(5))

        
        # STEP 5: CREATING A DERIVED ANALYSIS COLUMN
        
        
        df.loc[:, "total"] = df["quantity"] * df["price"]

        print("\n--- Verification Snapshot with Derived 'total' Revenue Column ---")
        print(df.head(5))

        # STEP 6: AGGREGATING DATA WITH GROUPBY & AGG
       
        print("\nAggregating order frequency blocks and financial matrices...")
        
       
        summary_df = df.groupby("product_id").agg({
            "line_item_id": "count",
            "total": "sum",
            "product_name": "first"
        })

        
        # STEP 7: CLEANING AND RE-LABELING HEADERS
       
        summary_df = summary_df.rename(columns={
            "line_item_id": "times_ordered",
            "total": "total_revenue"
        })

      
        # STEP 8: SORTING RESULTS ALPHABETICALLY
      
        summary_df = summary_df.sort_values(by="product_name", ascending=True)

        print("\n--- Final Aggregated & Sorted Order Summary Snapshot ---")
        print(summary_df.head(5))

       
        # STEP 9: WRITING DATA TO A SPREADSHEET FILE
        
        output_csv_path = "order_summary.csv"
        summary_df.to_csv(output_csv_path, index=True)
        print(f"\nSuccess! Order summary spreadsheet compiled cleanly to: {output_csv_path}")

   
    except sqlite3.Error as db_error:
       
        print(f"Database error encountered: {db_error}")
        
    except FileNotFoundError:
       
        print("File Error: Could not locate the lesson.db file inside the target ../db/ folder.")
        
    finally:
      
        if 'conn' in locals():
            conn.close()
            print("Lesson database communication safely disengaged.")



if __name__ == "__main__":
    main()
    
import numpy as np
import pandas as pd

arr1 = np.array([1, 2, 3, 4, 5])
print(f"From list: {arr1}")
print(f"Type: {type(arr1)}")

arr_zeros = np.zeros(5)
arr_ones = np.ones((2, 3))
arr_linspace = np.linspace(0, 1, 5)  
arr_random = np.random.randn(3, 3)  
arr_range = np.arange(0, 10, 2)  
print("Range:", arr_range)
print("Random:\n", arr_random)
print("Linspace:", arr_linspace)
print("Zeros:", arr_zeros)
print("Ones:\n", arr_ones)

'''Index and slicing'''

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print("array: ", arr)

print("Element at (0,0):", arr[0, 0])
print("Element at (1,2):", arr[1, 2])
print("First row:", arr[0, :])
print("Last column:", arr[:, -1])
print("Last column:",arr[:, -2])

# Broadcasting 
scaled_arr = arr + 5
print("Broadcasting (+5):", scaled_arr)

# Vectorized res
vec_result = arr * 2 
print("Vectorized result:", vec_result)
#  loop 
loop_result = [x * 2 for x in arr]

# 
np_nums = np.array([1, 2, 3], dtype=np.int64)
print("NumPy memory data type:", np_nums.dtype)

############################pandas########################
# SERIES 
s_list = pd.Series([10, 20, 30], name="Scores")
print("s_list series:",s_list)
s_dict = pd.Series({"a": 1, "b": 2})
print("s_dict sereis:",s_dict)
s_arr = pd.Series(np.array([100, 200]))
print("s_arr sereis:",s_arr)

df_arr = pd.DataFrame(np.random.rand(2, 2), columns=["Col1", "Col2"])
print(df_arr)

df = pd.DataFrame({
    "Name": ["Ali", "Bvgh", "ghjbj"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"]
})

print(df["Name"])
print("lable based fetching:",df.loc[0:1, ["Name", "Age"]])
print("position based selec:",df.iloc[0:2, 0:2])

# Boolean Ind
print(df[df["Age"] > 28])


data = pd.read_csv("data.csv")
print("limit:",data.head(10))
print("Data info",data.info())
print("Describe",data.describe())

data = data.drop_duplicates()
print("Missing values count", data.isnull().sum())
data = data.dropna(subset=['lat-lon'])
data['price'] = data['price'].fillna(data['price'].median())


property_summary = data.groupby("property_type").agg(
    total_properties=("property_type", "count"),
    avg_rooms=("rooms", "mean")
).reset_index()
print("property_summary:",property_summary)



comments = pd.read_csv("comments.csv")
data = pd.read_csv("data.csv")
posts=pd.read_csv("posts.csv")
import matplotlib.pyplot as plt

comments["post_id"] = comments["post_id"].astype(int)
posts["id"] = posts["id"].astype(int)
posts_comments_merged = pd.merge(comments, posts, left_on="post_id", right_on="id", suffixes=("_comment", "_post"))
print("posts_comments_merged:",posts_comments_merged)

comments_per_post = (
    posts_comments_merged.groupby(["post_id", "title"])
    .size()
    .reset_index(name="comment_count")
    .sort_values(by="comment_count", ascending=False)
)

print("--- Comments Per Post ---")
print(comments_per_post.to_string(index=False))


x = ["Post 1", "Post 2", "Post 3", "Post 4"]
y = [2, 5, 1, 4]

# plot
plt.figure(figsize=(8, 4))
plt.bar(x, y, color="skyblue")

plt.xlabel("Posts")
plt.ylabel("Comments")
plt.title("Simple Comments Bar Chart")
plt.show()
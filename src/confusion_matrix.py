from sklearn.metrics import confusion_matrix
import numpy as np

def main():
    prompt_list = read_in_csv("prompt")
    ortho_list = read_in_csv("ortho")
    hypo_list = read_in_csv("hypo")
    df_all_words = create_df_all_words(prompt_list,
                                       ortho_list,
                                       hypo_list)
    confusion_matrix = create_confusion_matrix(df_all_words)

def read_in_csv(type == "undefined"):
    if type == "undefined":
        print("No read in type defined")
    
    if platform.system().lower() == "linux":
        os_type = "linux"
    else:
        os_type = "windows"
    
    # Linux
    if os_type == "linux":
        if type == "prompt":

        elif type == "ortho":
        
        else:
             
             
    # Windows
    elif os_type == "windows":
        if type == "prompt":
        
        elif type == "ortho":
        
        else:
            file_path = "D:\repos\wav2vec-CHOREC\files\word_lists\2LG_words.csv"
            return

             

  


def create_confusion_matrix(df_all_words):
    # Example true labels and predicted labels
    prompt_orth_list = np.array([0, 1, 0, 1, 1, 0, 0])
    prompt_hypo_list = np.array([0, 1, 0, 1, 0, 1, 0])

    # Compute confusion matrix
    cm = confusion_matrix(prompt_orth_list,
                          prompt_hypo_list)
    
    # cm[0, 0] = TN
    # cm[0, 1] = FP
    # cm[1, 0] = FN
    # cm[1, 1] = TP
    print("Confusion Matrix:")
    print(cm)

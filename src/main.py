#Global imports
from global_imports import cv2, np, plt, Image, time
# import os
#Local imports
import preprocessing
import features
import classifiers
import prepare_data
import evaluations


def preprocess_feature(paths):
    '''
        + Main Pipeline starts here.
    '''
    global VERBOSE

    X_list = []
    y_list = []
    for author_i,tr in enumerate(paths):

        for image_i,image_path in enumerate(tr):
            if VERBOSE: print (f'image\t{image_i}\tof author:\t{author_i}')
            image = cv2.imread(image_path)
            list_images = preprocessing.preprocess(image)
            for img in list_images:
                # x = Image.fromarray(img)
                # x.show()
                img_wt = features.waveletTransform(img,'db1')
                his_of_line = features.LPB(img_wt,1,8)
                X_list.append(his_of_line)
                y_list.append(author_i)
            
    if VERBOSE: print(f'X shape:\t{len(X_list) , len(X_list[0])}')
    return np.array(X_list),np.array(y_list)
    



if __name__ == "__main__":
    # prepare_data.print_data_stat()

    VERBOSE = False
    DEBUG = False
    #fetch data
    accs = 0
    trials = 0
    while True:
        trials += 1
        train, test = prepare_data.fetch_data(mode='test', debug=DEBUG)
        X_tune, y_tune = preprocess_feature(train)
        X_test, y_test = preprocess_feature(test)
        accs += classifiers.call_svm(X_tune, y_tune, X_test, y_test, verbose=VERBOSE)
        print (f'Total trials: {trials}\t Correct Predictions: {accs}\tOverall Acc:{accs/trials}')
    
#global imports
from global_imports import cv2, np, PCA, StandardScaler

#local imports
import prepare_data     #step 0
import preprocessing    #step 1.1
import features         #step 1.2
import classifiers      #step 2
import evaluations

def step_0(_mode):
    '''
        + Fetches random images for either training or testing.
    '''
    return prepare_data.fetch_data(mode=_mode)
        

def step_1(paths, VERBOSE=False):
    '''
        + Main Pipeline starts here.
        + Takes a path to tune or test data and starts fetching, segmentation and features extraction.
        + Resulting X with rows representing lines and columns representing features.
        + and y vector that represent id of an author (0/1/2)
    '''
    
    X_list = []
    y_list = []
    for author_i,tr in enumerate(paths):
        for image_i, image_path in enumerate(tr):
            image = cv2.imread(image_path)
            list_images = preprocessing.preprocess(image)
            for img in list_images:
                # x = Image.fromarray(img)
                # x.show()
                coeffs = features.waveletTransform(img,'db4')
                cA ,(cH,cV,cD) = coeffs
                hist_of_line_horizontal = features.LPBH(cH,1,8)
                hist_of_line_vertical = features.LPBH(cV,1,8)
                hist_of_line_diagonal = features.LPBH(cD,1,8)

                # stacking histograms(features)
                hist_of_line = hist_of_line_horizontal + hist_of_line_vertical + hist_of_line_diagonal

                X_list.append(hist_of_line)
                y_list.append(author_i)
            
    if VERBOSE: print(f'X shape:\t{len(X_list) , len(X_list[0])}')
    return np.array(X_list),np.array(y_list)

def step_2(X_tune, X_test, y_tune,verbose=False):
    #scale
    sc = StandardScaler()
    X_tune = sc.fit_transform(X_tune)
    X_test = sc.transform(X_test)
    #pca
    pca = PCA(n_components=2, copy=False)
    X_tune = pca.fit_transform(X_tune)
    X_test = pca.transform(X_test)
    print (f'New Shapes: X_tune: {X_tune.shape}\ty_tune: {y_tune.shape}')
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)
    evaluations.plot_scatter_pca(X_tune, y_tune)
    return X_tune, X_test

def step_3(X_tune, y_tune, X_test, y_test, verbose=False, _mode='test', clf='svm'):
    '''
        + For now it's just a calling function, but later on, this will be passed the classifier technique
        used. and choose from it.
    '''
    if clf == 'svm':
        return classifiers.call_svm(X_tune, y_tune, X_test, y_test, verbose=verbose, _mode=_mode)


def pipe(feature='lbph', clf='svm', _mode='test', _verbose=False):
    '''
        + This is the main function call for this file.
        + It specifies which feature ext. technique and which classifier to be used.
    '''
    if _verbose: print ('\n\t\tFetch..')
    train, test = step_0(_mode=_mode)
    if _verbose: print ('\t\tPreprocess and FE..')
    X_tune, y_tune = step_1(train,_verbose)
    X_test, y_test = step_1(test,_verbose)
    if _verbose: print ('\t\tPCA..')
    X_tune,X_test = step_2(X_tune,X_test,y_tune, verbose=_verbose)
    if _verbose: print ('\t\tCLF..')
    pre, acc = step_3(X_tune, y_tune, X_test, y_test, verbose=_verbose, _mode=_mode, clf=clf)
    return pre, acc
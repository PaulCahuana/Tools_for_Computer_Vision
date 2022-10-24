from openvino.runtime import Core
from openvino.preprocess import PrePostProcessor, ColorFormat
from openvino.runtime import Core, Layout, Type

import cv2
import numpy as np

def create_preprocess_configuration(  net):
    """ This method creates the pre processing configuration that will be passed through
    the image at the beginning of the inference process

    Args:
        config: Image to be pre-processed
        net: Model loaded

    Returns:
        A configuration with the pre-processing methods that will be passed through the network
    """
    input_scale=1
    size=[1,160,160,3]
    mean_scalar=()
    swap_rb=False
    crop=False
    ddepth = cv2.CV_32F

    pre_post_processor = PrePostProcessor(net)

    pre_post_processor.input().tensor() \
    .set_element_type(Type.f32) \
    .set_layout(Layout('NHWC')) \
    .set_color_format(ColorFormat.BGR)

    if not len(mean_scalar) == 0:
        pre_post_processor.input().preprocess().mean(mean_scalar)

    if type(input_scale) == list:
        pre_post_processor.input().preprocess().scale(input_scale)
    elif not input_scale == 1.0:
        pre_post_processor.input().preprocess().scale(1.0 / input_scale)

    if (swap_rb):
        pre_post_processor.input().preprocess().convert_color(ColorFormat.RGB)

    pre_post_processor.input().model().set_layout(Layout('??HW'))

    return pre_post_processor, size

def preprocess( img,size):
    """ This pre-process method just resize the image to the correct
    input size and expand the dimensions to pass through the OpenVINO model
    Args:
        config: Image to be pre-processed
    Returns:
        An image with additional batch dimension and resized
    """
    final_img = img.copy()
    final_img = cv2.resize(final_img, (size[1], size[2]))
    final_img=np.expand_dims(final_img, 0)
    print("final_img: ",final_img.shape)
    return final_img
def predict_single( output):
    """ This method receives the output and returns
    a more cleaned version more easy to iterate over

    Args:
        output: the raw output of the model

    Returns:
        The cleaned output of the model
    """
    return output[list(output.keys())[0]]

def predict( img, compiled_net,size, with_preprocess=True):
    """ The predict method receives an img and run
    the inference returning the output of the network

    Args:
        img: Image to be infer
        with_preprocess: Change this parameter to enable/disable the preprocessing
    Returns:
        Output of the network
    """
    if with_preprocess:
        img_ = preprocess(img,size)
    else:
        img_ = img.copy()
    
    output = compiled_net([img_])
    if len(output) > 1:
        return output
    else:
        return predict_single(output)

def inference(model_name,image_test,framework):
    if framework=="OPENVINO_ONNX":
        ie = Core()  
        if   framework == "OPENVINO_ONNX":
            print("Working OpenVino with ONNX ")
            print()
            net = ie.read_model(model=model_name+".onnx")
        elif framework == "OPENVINO":
            print("Working only OpenVino")
            print()
            net = ie.read_model(model=model_name+".xml", weights=model_name+".bin")

        pre_post_processor, size = create_preprocess_configuration( net)
        net = pre_post_processor.build()

        compiled_net = ie.compile_model(net, "CPU")

        output_prediction=predict(image_test,compiled_net,size)
        print("output_prediction: ",output_prediction)
    elif ""



model_name = "face_landmark_160x160"
image_test="datasets/face_paul.jpg"
image_test = cv2.imread(image_test)
framework="OPENVINO_ONNX" # OPENVINO    ONNX
inference(model_name,image_test,framework)
#cv2.imshow('img ',image_test)
#if cv2.waitKey(0) & 0xFF == ord("q"):
#    cv2.destroyAllWindows()
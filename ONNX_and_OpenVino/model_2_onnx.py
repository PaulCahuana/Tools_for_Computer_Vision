import torch
import torch.onnx 


def Convert_ONNX(model): 

    # set the model to inference mode 
    model.eval() 
    model.to("cpu")

    # Let's create a dummy input tensor  
    dummy_input = torch.randn(1, 3,256,256, requires_grad=False).cpu()
    #print("dummy_input: ",dummy_input)
    # Export the model 
    print("model.module: ",model)
      
    torch.onnx.export(model.module,         # model being run 
         dummy_input,       # model input (or a tuple for multiple inputs) 
         "hrnet_fixed_2.onnx",       # where to save the model  
         opset_version=11)    # the ONNX version to export the model to ) 
    print(" ") 
    print('Model has been converted to ONNX')
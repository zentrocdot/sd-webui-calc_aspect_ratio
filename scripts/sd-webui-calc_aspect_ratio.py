'''sd-webui-calc_aspect_ratio
Extension for AUTOMATIC1111.

Version 0.0.0.1
'''
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=import-error
# pylint: disable=consider-using-from-import
# pylint: disable=trailing-whitespace
# pylint: disable=unused-argument
# pylint: disable=too-many-instance-attributes
# pylint: disable=no-self-use

# Import the Python modules.
import contextlib
import gradio as gr
import modules.scripts as scripts
from modules.ui_components import InputAccordion
   
# Define class CalcAspectRatioScript.
class CalcAspectRatioScript(scripts.Script):
    '''Class for calculating the aspect ratio.'''
    
    def title(self):
        '''Class method title.'''
        return "Aspect Ratio Calculator"

    def show(self, is_img2img):
        '''Class method show.'''
        return scripts.AlwaysVisible  # hide this script in the Scripts dropdown

    def image_resolution(self, is_img2img):
        '''Get the image resolution from container and return the values.'''
        if is_img2img:
            imgres = [self.i2i_w, self.i2i_h]
        else:
            imgres = [self.t2i_w, self.t2i_h]
        return imgres  

    def ui(self, is_img2img):
        '''Class method ui.'''
        # Set the css format strings.
        css_acc = f'{"img" if is_img2img else "txt"}2img_sc_accordion_aspect_ratio'
        css_col = f'{"img" if is_img2img else "txt"}2img_sc_column_aspect_ratio'
        css_row = f'{"img" if is_img2img else "txt"}2img_sc_row_aspect_ratio'        
        # Create a column.
        with gr.Column(elem_id=css_col):
            # Create an accordioan.
            with InputAccordion(
                False, label="Calculate Aspect Ratio", elem_id=css_acc
            ) as enabled:
                arvalue = gr.Textbox(value="N/A", lines=1, 
                    label="Calculated aspect ratio from Width/Height", interactive=False, inputs=None
                )
                # Create a row.
                with gr.Row(elem_id=css_row):
                    mybutton = gr.Button("Acquire Width and Height")          
                    with contextlib.suppress(AttributeError):
                        imgres = self.image_resolution(is_img2img)
                        def update_number(x,y):
                            if x > y:
                                z = x/y
                                if float(z).is_integer():
                                    z = int(z)                                 
                                ret = str(z) + ":1"                   
                            elif x <= y:
                                z = y/x
                                if float(z).is_integer():
                                    z = int(z)
                                ret = "1:" + str(z)    
                            return str(ret)
                        mybutton.click(update_number, inputs=imgres, outputs=arvalue)               
          
    # Class method after_component.
    def after_component(self, component, **kwargs):
        '''Class method after_component.

        This method is used to generalize the existing programme code. It is
        detected if one is in the txt2img tab or in the img2img tab. Then the
        corresponding self variables can be used in the same programme code 
        for both tabs.
        '''
        if kwargs.get("elem_id") == "txt2img_width":
            self.t2i_w = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.t2i_h = component
        if kwargs.get("elem_id") == "img2img_width":
            self.i2i_w = component
        if kwargs.get("elem_id") == "img2img_height":
            self.i2i_h = component
        if kwargs.get("elem_id") == "img2img_image":
            self.image = [component]
        if kwargs.get("elem_id") == "img2img_sketch":
            self.image.append(component)
        if kwargs.get("elem_id") == "img2maskimg":
            self.image.append(component)
        if kwargs.get("elem_id") == "inpaint_sketch":
            self.image.append(component)
        if kwargs.get("elem_id") == "img_inpaint_base":
            self.image.append(component)

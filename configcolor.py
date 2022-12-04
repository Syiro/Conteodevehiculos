from PIL import Image, ImageEnhance, ImageOps
class ConfigColor:
    def __init__(self,brillo,contraste,color):
        self.brillo=brillo
        self.contrate=contraste
        self.color=color
        
    def configbrillo(self,path,brillo):
        
        im = Image.open(path)
        #image brightness enhancer
        enhancer = ImageEnhance.Brightness(im)
        factor = brillo/10.0
        im_output = enhancer.enhance(factor)
        pathout = "original-image.png"
        im_output.save(pathout)
        return pathout
    
    def configcontraste(self,path,contraste):
        im = Image.open(path)
        #image brightness enhancer
        enhancer = ImageEnhance.Sharpness(im)
        factor = contraste/10.0#gives original image
        im_output = enhancer.enhance(factor)
        pathout = "original-image.png"
        im_output.save(pathout)
        return pathout
    
    def configcolor(self,path,color):
        im = Image.open(path)
        #image brightness enhancer
        enhancer = ImageEnhance.Color(im)
        factor = color/10.0 #gives original image
        im_output = enhancer.enhance(factor)
        pathout = "original-image.png"
        im_output.save(pathout)
        return pathout
    
    # def converter_image(self,path,brillo,contraste,color):
    #     contrast_converter = ImageEnhance.Contrast(path)
    #     img_b = contrast_converter.enhance(contraste)
    #     brightness_converter = ImageEnhance.Brightness(img_b)
    #     img_c = brightness_converter.enhance(brillo)
    #     color_converter = ImageEnhance.Color(img_c)
    #     img_d = color_converter.enhance(color)
    #     img_final=img_d
    #     return img_final
        


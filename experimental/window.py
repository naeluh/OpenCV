import time, cv2

class Window(object):
    _window_name = None
    parent = None
    def __init__(self, debug=True, processors=[]):
        self.debug = debug
        self.processors = processors
        self.log('Init capture')

    def add_trackbar(self,trackbar):
        trackbar.parent = self if not self.parent else self.parent
        cv2.createTrackbar(trackbar.name,trackbar.window_name,trackbar.default,trackbar.max,trackbar._set_value)

    def log (self,message):
        if self.debug: print '%s: %s'%(self.window_name,message)

    def get_source (self):
        return None

    def _set_window_name (self,name):
        self._window_name = name

    def _get_window_name(self):
        return self._window_name if self._window_name else '%s - %s' % (self.__class__.__name__,id(self))

    window_name = property(_get_window_name,_set_window_name)

    def show(self):
        cv2.namedWindow(self.window_name)
        for processor in self.processors:
            processor.contribute_to_test(self)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

    def on_mouse(self,*args,**kwargs):
        for processor in self.processors:
            processor.on_mouse(*args,**kwargs)

    def on_key(self,key):
        for processor in self.processors:
            processor.on_key(key)

    def paint (self,source):
        img = source
        try:
            before = time.time()
            for processor in self.processors:
                img = processor.process(img)
                if img == None: raise Exception('Processor %s doesnt return any image'%processor.__class__.__name__)
            # img.dtype = np.uint8
            fps = 1/(time.time()-before)
            if self.debug:
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(255, 255, 255), thickness = 1, linetype=cv2.CV_AA)        

        except Exception, e:
            # img = cv2.cvtColor(source,cv2.COLOR_GRAY2RGB)
            img = source
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 255), thickness = 1, linetype=cv2.CV_AA)        

            self.log('Exception ocurred: %s'%str(e))

        cv2.imshow(self.window_name,img)


class NavController:

    def __init__(self, view, video_controller):
        self.video_controller = video_controller
        self.view = view
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.sig_nav_videos.connect(self.view.show_videos_page)
        self.view.sig_nav_diapositivas.connect(self.view.show_diapositivas_page)

    def start_app(self):
        self.view.show()

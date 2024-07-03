import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        self._listYear = self._model.getAnni()
        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

    def fillDD2(self, e):
        self._listShape = self._model.getForme(self._view.ddyear.value)
        for a in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        if anno is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere l'anno."))
            return
        forma = self._view.ddshape.value
        if forma is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere la forma."))
            return

        self._model.buildGraph(anno, forma)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} vertici."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))

        tupla = self._model.getPesiAdiacenti()
        for t in tupla:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {t[0].id}, somma pesi su archi: {t[1]}"))

        self._view.update_page()


    def handle_path(self, e):
        self._model.getPath()
        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0].id} --> {ii[1].id}: weight {ii[2]} distance {str(self._model.get_distance_weight(ii))}"))  # ii[2]

        self._view.update_page()

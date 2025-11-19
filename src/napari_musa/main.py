import napari
import numpy as np  # <--- QUI era sbagliato prima
from qtpy.QtCore import QTimer

from napari_musa.modules.data import Data
from napari_musa.modules.plot import Plot
from napari_musa.Widget_DataManager import DataManager
from napari_musa.Widgets_DataVisualization import DataVisualization
from napari_musa.Widgets_EndmembersExtraction import EndmembersExtraction
from napari_musa.Widgets_Fusion import Fusion
from napari_musa.Widgets_NMF import NMF
from napari_musa.Widgets_PCA import PCA
from napari_musa.Widgets_UMAP import UMAP


def setup_connections(
    viewer, datamanager_widget, endmextr_widget, nmf_widget, pca_widget
):
    """"""
    viewer.text_overlay.visible = True

    def on_step_change(event=None):
        layer = viewer.layers.selection.active
        if layer and isinstance(layer, napari.layers.Image):
            name = layer.name
            if "NNLS" in name or "SAM" in name:
                endmextr_widget.update_number_H()
            elif "NMF" in name:
                nmf_widget.update_number_H()
            elif "PCA" in name:
                pca_widget.update_number_H()
            else:
                datamanager_widget.update_wl()

    viewer.dims.events.current_step.connect(on_step_change)

    viewer.layers.selection.events.active.connect(
        datamanager_widget.layer_auto_selection
    )


def make_on_new_layer(viewer):
    """Factory per il callback, così ha accesso a `viewer` via closure."""

    def on_new_layer(event):
        layer = event.value
        if (
            isinstance(layer, napari.layers.Labels) and layer.data.ndim == 3
        ):  # (C, Y, X)

            def replace():
                if layer in viewer.layers:  # solo se esiste ancora
                    new_labels = np.zeros(layer.data.shape[1:], dtype=np.int32)
                    name = layer.name
                    viewer.layers.remove(layer)
                    viewer.add_labels(new_labels, name=name)

            QTimer.singleShot(0, replace)

    return on_new_layer


def make_update_modes_comboboxes(
    data,
    datamanager_widget,
    umap_widget,
    fusion_widget,
    endmextr_widget,
    pca_widget,
    nmf_widget,
):
    """Factory per aggiornare tutte le combobox dei 'modes'."""

    widgets = [
        datamanager_widget,
        umap_widget,
        fusion_widget,
        endmextr_widget,
        pca_widget,
        nmf_widget,
    ]

    def update_modes_comboboxes(*_):
        for widget in widgets:
            for attr_name in dir(widget):
                if attr_name.startswith("modes_combobox"):
                    if widget == fusion_widget:
                        widget.modes_combobox_1.choices = data.modes
                        widget.modes_combobox_2.choices = data.modes
                        widget.modes_combobox_3.choices = data.modes
                    else:
                        current_value = widget.modes_combobox.value
                        widget.modes_combobox.choices = data.modes
                        if current_value not in data.modes:
                            widget.modes_combobox.value = current_value

    return update_modes_comboboxes


def run_napari_app():
    """Add widgets to the viewer"""
    try:
        viewer = napari.current_viewer()
    except AttributeError:
        viewer = napari.Viewer()

    # WIDGETS
    data = Data()
    plot_datavisualization = Plot(viewer=viewer, data=data)
    datamanager_widget = DataManager(viewer, data)
    datavisualization_widget = DataVisualization(
        viewer, data, plot_datavisualization, datamanager_widget
    )
    fusion_widget = Fusion(viewer, data)

    plot_umap = Plot(viewer=viewer, data=data)
    umap_widget = UMAP(viewer, data, plot_umap)
    nmf_widget = NMF(viewer, data, plot_umap)
    endmextr_widget = EndmembersExtraction(viewer, data, plot_umap)
    plot_pca = Plot(viewer=viewer, data=data)
    pca_widget = PCA(viewer, data, plot_pca)

    update_modes_comboboxes = make_update_modes_comboboxes(
        data,
        datamanager_widget,
        umap_widget,
        fusion_widget,
        endmextr_widget,
        pca_widget,
        nmf_widget,
    )
    datamanager_widget.mode_added.connect(update_modes_comboboxes)

    # Add widget as dock
    datamanager_dock = viewer.window.add_dock_widget(
        datamanager_widget, name="Data Manager", area="right"
    )
    datavisualization_dock = viewer.window.add_dock_widget(
        datavisualization_widget, name="Data Visualization", area="right"
    )
    fusion_dock = viewer.window.add_dock_widget(
        fusion_widget, name="Fusion", area="right"
    )
    umap_dock = viewer.window.add_dock_widget(
        umap_widget, name="UMAP", area="right"
    )
    endmextr_dock = viewer.window.add_dock_widget(
        endmextr_widget, name="Endmembers", area="right"
    )
    pca_dock = viewer.window.add_dock_widget(
        pca_widget, name="PCA", area="right"
    )
    nmf_dock = viewer.window.add_dock_widget(
        nmf_widget, name="NMF", area="right"
    )

    # Tabify the widgets
    viewer.window._qt_window.tabifyDockWidget(
        datamanager_dock, datavisualization_dock
    )
    viewer.window._qt_window.tabifyDockWidget(
        datavisualization_dock, fusion_dock
    )
    viewer.window._qt_window.tabifyDockWidget(fusion_dock, umap_dock)
    viewer.window._qt_window.tabifyDockWidget(umap_dock, pca_dock)
    viewer.window._qt_window.tabifyDockWidget(pca_dock, endmextr_dock)
    viewer.window._qt_window.tabifyDockWidget(endmextr_dock, nmf_dock)

    # Text overlay in the viewer
    viewer.text_overlay.visible = True

    # Connections
    setup_connections(
        viewer, datamanager_widget, endmextr_widget, nmf_widget, pca_widget
    )
    viewer.layers.events.inserted.connect(make_on_new_layer(viewer))
    viewer.layers.selection.events.active.connect(
        datamanager_widget.on_layer_selected
    )

    return None

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QFrame, QSizePolicy, QScrollArea, 
    QTabWidget, QComboBox, QGridLayout, QStackedWidget
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#2a2a40')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#2a2a40')
        
        # Style the chart
        self.fig.patch.set_facecolor('#2a2a40')
        self.axes.spines['bottom'].set_color('#ffffff')
        self.axes.spines['top'].set_color('#2a2a40') 
        self.axes.spines['right'].set_color('#2a2a40')
        self.axes.spines['left'].set_color('#ffffff')
        self.axes.tick_params(axis='x', colors='#ffffff')
        self.axes.tick_params(axis='y', colors='#ffffff')
        self.axes.yaxis.label.set_color('#ffffff')
        self.axes.xaxis.label.set_color('#ffffff')
        self.axes.title.set_color('#ffffff')
        
        super(MplCanvas, self).__init__(self.fig)


class InsightCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2a2a40;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Card title
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #ffffff; padding-bottom: 10px;")
        
        # Add title to layout
        self.layout.addWidget(self.title_label)
        
        # This will be overridden by child classes
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.layout.addWidget(self.content_widget)


class ManufacturersCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("Most Popular EV Manufacturers", parent)
        
        # Create chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        top_manufacturers = df['Make'].value_counts().head(10)
        
        # Create bars with gradient colors
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_manufacturers)))
        bars = self.canvas.axes.bar(top_manufacturers.index, top_manufacturers.values, color=colors)
        
        # Style chart
        self.canvas.axes.set_ylabel('Number of Vehicles')
        self.canvas.axes.set_title('Top 10 EV Manufacturers')
        plt.setp(self.canvas.axes.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            self.canvas.axes.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', color='white')
                    
        self.canvas.fig.tight_layout()
        
        # Add insight text
        insight_text = """
        <p style='color:#aaffaa;'>✓ Insight:</p>
        <p>Tesla is the leading EV manufacturer in Washington, followed by Nissan, 
        Chevrolet, and Ford. This indicates Tesla's strong market presence in the 
        EV domain within the state.</p>
        """
        self.insight_label = QLabel(insight_text)
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px;")
        
        # Add to layout
        self.content_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.insight_label)


class RegistrationsByYearCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("Number of EVs Registered Each Year", parent)
        
        # Create chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        ev_count_by_year = df['Model Year'].value_counts().sort_index()
        
        # Create line chart
        self.canvas.axes.plot(ev_count_by_year.index, ev_count_by_year.values, 
                             marker='o', linestyle='-', linewidth=2, color='#00aaff')
        
        # Fill area under the line
        self.canvas.axes.fill_between(ev_count_by_year.index, ev_count_by_year.values, 
                                     alpha=0.3, color='#00aaff')
        
        # Style chart
        self.canvas.axes.set_xlabel('Year')
        self.canvas.axes.set_ylabel('Number of Registrations')
        self.canvas.axes.set_title('EV Registrations by Year')
        self.canvas.fig.tight_layout()
        
        # Add insight text
        insight_text = """
        <p style='color:#aaffaa;'>✓ Insight:</p>
        <p>There has been a significant increase in EV registrations since 2018, 
        showing a growing interest in electric vehicles and a shift towards 
        sustainable transportation.</p>
        """
        self.insight_label = QLabel(insight_text)
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px;")
        
        # Add to layout
        self.content_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.insight_label)


class EVTypeDistributionCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("Distribution of EV Types (BEV vs PHEV)", parent)
        
        # Create chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        ev_types = df['Electric Vehicle Type'].value_counts()
        
        # Create pie chart with custom colors
        colors = ['#8844ee', '#ff6644']
        explode = (0.1, 0)  # explode the 1st slice (BEV)
        
        self.canvas.axes.pie(ev_types.values, explode=explode, labels=ev_types.index, 
                            autopct='%1.1f%%', startangle=90, colors=colors, 
                            wedgeprops={'edgecolor': '#2a2a40'})
        
        self.canvas.axes.set_title('EV Type Distribution')
        self.canvas.axes.axis('equal')  # Equal aspect ratio ensures pie is circular
        self.canvas.fig.tight_layout()
        
        # Add insight text
        insight_text = """
        <p style='color:#aaffaa;'>✓ Insight:</p>
        <p>Battery Electric Vehicles (BEVs) dominate the market, comprising the majority 
        of EVs registered. Plug-in Hybrid Electric Vehicles (PHEVs) form a smaller, 
        yet notable portion.</p>
        """
        self.insight_label = QLabel(insight_text)
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px;")
        
        # Add to layout
        self.content_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.insight_label)


class CountiesCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("Top Counties with the Most EVs", parent)
        
        # Create chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        top_counties = df['County'].value_counts().head(10)
        
        # Create horizontal bar chart with gradient
        colors = plt.cm.cool(np.linspace(0.2, 0.8, len(top_counties)))
        bars = self.canvas.axes.barh(top_counties.index[::-1], top_counties.values[::-1], color=colors[::-1])
        
        # Style chart
        self.canvas.axes.set_xlabel('Number of EVs')
        self.canvas.axes.set_title('Top 10 Counties by EV Registration')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            self.canvas.axes.text(width + 5, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center', color='white')
        
        self.canvas.fig.tight_layout()
        
        # Add insight text
        insight_text = """
        <p style='color:#aaffaa;'>✓ Insight:</p>
        <p>King County has the highest number of registered EVs, followed by 
        Snohomish, Pierce, and Clark counties. Urban and suburban regions show 
        greater EV adoption.</p>
        """
        self.insight_label = QLabel(insight_text)
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px;")
        
        # Add to layout
        self.content_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.insight_label)


class RangeByYearCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("Correlation Between Electric Range and Model Year", parent)
        
        # Create chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        
        # Check if Electric Range column exists
        if 'Electric Range' in df.columns:
            # Group by year and calculate average range
            range_by_year = df.groupby('Model Year')['Electric Range'].mean()
            
            # Create scatter plot with trend line
            self.canvas.axes.scatter(range_by_year.index, range_by_year.values, 
                                    color='#ff5588', s=50, alpha=0.7)
            
            # Add trend line
            z = np.polyfit(range_by_year.index, range_by_year.values, 1)
            p = np.poly1d(z)
            self.canvas.axes.plot(range_by_year.index, p(range_by_year.index), 
                                 linestyle='--', color='#ffffff', alpha=0.8)
            
            # Style chart
            self.canvas.axes.set_xlabel('Model Year')
            self.canvas.axes.set_ylabel('Average Electric Range (miles)')
            self.canvas.axes.set_title('Electric Range by Model Year')
            
            # Add annotation showing the trend
            x_pos = range_by_year.index.max() - 2
            y_pos = p(x_pos) + 10
            self.canvas.axes.annotate(f'Trend: {z[0]:.2f} miles/year', 
                                     xy=(x_pos, p(x_pos)),
                                     xytext=(x_pos, y_pos),
                                     color='white',
                                     arrowprops=dict(facecolor='white', shrink=0.05, alpha=0.7))
            
            self.canvas.fig.tight_layout()
        else:
            self.canvas.axes.text(0.5, 0.5, "Electric Range data not available", 
                                 ha='center', va='center', color='white', fontsize=12)
        
        # Add insight text
        insight_text = """
        <p style='color:#aaffaa;'>✓ Insight:</p>
        <p>Newer model years tend to have higher electric ranges, reflecting 
        technological improvements in battery efficiency and vehicle performance.</p>
        """
        self.insight_label = QLabel(insight_text)
        self.insight_label.setWordWrap(True)
        self.insight_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px;")
        
        # Add to layout
        self.content_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.insight_label)


class SummaryCard(InsightCard):
    def __init__(self, df, parent=None):
        super().__init__("EV Dashboard Summary", parent)
        
        # Calculate key metrics
        total_evs = len(df)
        num_manufacturers = df['Make'].nunique()
        bev_count = df[df['Electric Vehicle Type'] == 'Battery Electric Vehicle (BEV)'].shape[0]
        phev_count = df[df['Electric Vehicle Type'] == 'Plug-in Hybrid Electric Vehicle (PHEV)'].shape[0]
        bev_percentage = (bev_count / total_evs) * 100 if total_evs > 0 else 0
        
        # Create metrics display
        metrics_layout = QGridLayout()
        
        # Helper function to create metric widgets
        def create_metric(title, value, unit=""):
            frame = QFrame()
            frame.setStyleSheet("background-color: #3a3a50; border-radius: 10px;")
            layout = QVBoxLayout(frame)
            
            value_label = QLabel(f"{value}{unit}")
            value_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet("color: #ffffff;")
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 10))
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("color: #aaaaaa;")
            
            layout.addWidget(value_label)
            layout.addWidget(title_label)
            
            return frame
        
        # Add metrics
        metrics_layout.addWidget(create_metric("Total EVs", f"{total_evs:,}"), 0, 0)
        metrics_layout.addWidget(create_metric("Manufacturers", f"{num_manufacturers}"), 0, 1)
        metrics_layout.addWidget(create_metric("BEV Count", f"{bev_count:,}"), 1, 0)
        metrics_layout.addWidget(create_metric("PHEV Count", f"{phev_count:,}"), 1, 1)
        metrics_layout.addWidget(create_metric("BEV Percentage", f"{bev_percentage:.1f}", "%"), 2, 0, 1, 2)
        
        # Add to content layout
        self.content_layout.addLayout(metrics_layout)
        
        # Add overall summary text
        summary_text = """
        <p style='color:#aaffaa;'>✓ Executive Summary:</p>
        <p>Washington State shows strong adoption of electric vehicles, with BEVs being
        the dominant choice. Tesla leads the market, and there's a clear upward trend in 
        EV registrations since 2018. Urban areas like King County show the highest 
        adoption rates, and technological improvements are evident in the increasing 
        electric range of newer models.</p>
        """
        self.summary_label = QLabel(summary_text)
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("color: #ffffff; background-color: #202030; padding: 10px; border-radius: 5px; margin-top: 15px;")
        
        self.content_layout.addWidget(self.summary_label)


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EV Analysis Dashboard - Washington State")
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.setGeometry(100, 100, 1200, 800)
        
        # Load data
        try:
            self.df = pd.read_csv('ev_population.csv')
            self.df.dropna(subset=['Make', 'Model', 'Model Year', 'Electric Vehicle Type'], inplace=True)
            self.df['Model Year'] = self.df['Model Year'].astype(int)
            self.df.columns = self.df.columns.str.strip()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()  # Empty DataFrame as fallback
        
        # Set up central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Initialize UI components
        self.init_sidebar()
        self.init_main_area()
        
    def init_sidebar(self):
        # Create sidebar container
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(80)
        sidebar_widget.setStyleSheet("background-color: #12121c; border-radius: 15px;")
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)
        sidebar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        
        # App logo/icon
        logo_label = QLabel()
        logo_label.setPixmap(self.style().standardIcon(QApplication.style().SP_ComputerIcon).pixmap(32, 32))
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #333344;")
        separator.setFixedHeight(1)
        sidebar_layout.addWidget(separator)
        sidebar_layout.addSpacing(15)
        
        # Navigation buttons
        button_style = """
            QPushButton {
                background-color: #252535;
                border-radius: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #353545;
            }
            QPushButton:pressed {
                background-color: #4444aa;
            }
        """
        
        # Dashboard button (selected by default)
        self.dashboard_btn = QPushButton()
        self.dashboard_btn.setIcon(self.style().standardIcon(QApplication.style().SP_FileDialogDetailedView))
        self.dashboard_btn.setIconSize(QSize(24, 24))
        self.dashboard_btn.setFixedSize(50, 50)
        self.dashboard_btn.setStyleSheet(button_style + "background-color: #4444aa;")
        self.dashboard_btn.setToolTip("Dashboard")
        self.dashboard_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        # Charts button
        self.charts_btn = QPushButton()
        self.charts_btn.setIcon(self.style().standardIcon(QApplication.style().SP_FileDialogInfoView))
        self.charts_btn.setIconSize(QSize(24, 24))
        self.charts_btn.setFixedSize(50, 50)
        self.charts_btn.setStyleSheet(button_style)
        self.charts_btn.setToolTip("Charts")
        self.charts_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Map button
        self.map_btn = QPushButton()
        self.map_btn.setIcon(self.style().standardIcon(QApplication.style().SP_DirIcon))
        self.map_btn.setIconSize(QSize(24, 24))
        self.map_btn.setFixedSize(50, 50)
        self.map_btn.setStyleSheet(button_style)
        self.map_btn.setToolTip("Map View")
        self.map_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # Settings button
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(self.style().standardIcon(QApplication.style().SP_FileDialogListView))
        self.settings_btn.setIconSize(QSize(24, 24))
        self.settings_btn.setFixedSize(50, 50)
        self.settings_btn.setStyleSheet(button_style)
        self.settings_btn.setToolTip("Settings")
        
        # Add buttons to sidebar
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.charts_btn)
        sidebar_layout.addWidget(self.map_btn)
        sidebar_layout.addWidget(self.settings_btn)
        
        # Add spacer at the bottom
        sidebar_layout.addStretch()
        
        # Add user icon at bottom
        user_btn = QPushButton()
        user_btn.setIcon(self.style().standardIcon(QApplication.style().SP_DialogApplyButton))
        user_btn.setIconSize(QSize(24, 24))
        user_btn.setFixedSize(50, 50)
        user_btn.setStyleSheet(button_style)
        user_btn.setToolTip("User Profile")
        sidebar_layout.addWidget(user_btn)
        
        # Add sidebar to main layout
        self.main_layout.addWidget(sidebar_widget)
    
    def init_main_area(self):
        # Create main content area
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #1e1e2f;")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header area
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("EV Analysis Dashboard")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_layout.addWidget(title_label)
        
        # Add some spacing
        header_layout.addStretch()
        
        # Search bar (non-functional in this demo)
        search_combo = QComboBox()
        search_combo.setFixedWidth(200)
        search_combo.setStyleSheet("""
            QComboBox {
                background-color: #252535;
                border-radius: 10px;
                padding: 8px;
                color: white;
            }
        """)
        search_combo.addItem("Washington State")
        header_layout.addWidget(search_combo)
        
        # Add header to main layout
        main_layout.addLayout(header_layout)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        
        # Add dashboard page
        self.create_dashboard_page()
        
        # Add charts page
        self.create_charts_page()
        
        # Add map page (placeholder)
        map_page = QWidget()
        map_layout = QVBoxLayout(map_page)
        map_layout.addWidget(QLabel("Map View - Coming Soon"))
        self.stacked_widget.addWidget(map_page)
        
        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)
        
        # Add main widget to main layout
        self.main_layout.addWidget(main_widget)
    
    def create_dashboard_page(self):
        # Create dashboard page with summary and key metrics
        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)
        
        # Create scroll area for dashboard content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1e1e2f;
            }
            QScrollBar:vertical {
                background: #252535;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4444aa;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create container for scroll area content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add summary card
        summary_card = SummaryCard(self.df)
        scroll_layout.addWidget(summary_card)
        
        # Create grid layout for insight cards
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # Add cards to grid
        grid_layout.addWidget(ManufacturersCard(self.df), 0, 0)
        grid_layout.addWidget(RegistrationsByYearCard(self.df), 0, 1)
        grid_layout.addWidget(EVTypeDistributionCard(self.df), 1, 0)
        grid_layout.addWidget(CountiesCard(self.df), 1, 1)
        grid_layout.addWidget(RangeByYearCard(self.df), 2, 0, 1, 2)
        
        # Add grid to scroll layout
        scroll_layout.addLayout(grid_layout)
        
        # Set scroll content
        scroll_area.setWidget(scroll_content)
        
        # Add scroll area to dashboard layout
        dashboard_layout.addWidget(scroll_area)
        
        # Add dashboard page to stacked widget
        self.stacked_widget.addWidget(dashboard_page)
    
    def create_charts_page(self):
        # Create detailed charts page with tabs
        charts_page = QWidget()
        charts_layout = QVBoxLayout(charts_page)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333344;
                background-color: #1e1e2f;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #252535;
                color: #aaaaaa;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4444aa;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #353545;
            }
        """)
        
        # Create tabs for each chart type
        for i, (title, widget_class) in enumerate([
            ("Manufacturers", ManufacturersCard),
            ("Yearly Registrations", RegistrationsByYearCard),
            ("EV Types", EVTypeDistributionCard),
            ("Counties", CountiesCard),
            ("Range by Year", RangeByYearCard)
        ]):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.addWidget(widget_class(self.df))
            tab_widget.addTab(tab, title)
        
        # Add tab widget to charts layout
        charts_layout.addWidget(tab_widget)
        
        # Add charts page to stacked widget
        self.stacked_widget.addWidget(charts_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Apply modern style
    app.setStyle("Fusion")
    # Set app-wide dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 47))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 40))
    dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 55))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(42, 42, 64))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(37, 37, 59))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    # Create and show dashboard
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
from window import Ui_MainWindow
from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import psutil
import sys
import datetime
import platform
import shutil
from time import sleep

platforms = {
  'linux':'Linux',
  'linux1':'Linux',
  'linux2':'Linux',
  'darwin':'OS X',
  'win32':'Windows'
}

class SystemMonitor(QMainWindow, Ui_MainWindow):
  def __init__(self) -> None:
    super().__init__()
    self.setupUi(self)

    #region Data
    self.Cat_label_list=[self.label_11,self.label_15,self.label_19,self.label_9,self.label_21,self.label_7,self.label_13]
    self.Cat_list = [self.cpu,self.battary,self.activities,self.storage,self.sensor,self.network,self.sysInfo]
    #endregion

    # Header Buttons Functions
    self.label_3.clicked.connect(self.close)
    self.label_5.clicked.connect(self.Maximized_or_Minimized)
    self.label_4.clicked.connect(self.showMinimized)

    # Window ReSizing And Move
    self.frame.mousePressEvent = self.Cat_Size
    self.header.mouseMoveEvent = self.Move_Window

    #region Category Acctivate Pages
    self.cpu.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(0) or self.active_cat(self.cpu)
    self.activities.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(3) or self.active_cat(self.activities)
    self.battary.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(1) or self.active_cat(self.battary)
    self.network.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(6) or self.active_cat(self.network)
    self.sensor.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(5) or self.active_cat(self.sensor)
    self.storage.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(4) or self.active_cat(self.storage)
    self.sysInfo.mousePressEvent = lambda a: self.stackedWidget.setCurrentIndex(2) or self.active_cat(self.sysInfo)
    #endregion

    self.finisher()

  def sec2hour(self , secs):
    h = int(secs/3600)
    secs = secs - h*3600
    m = int(secs/60)
    secs = secs - m*60
    s = secs
    return f"{h} H {m} Min {s} Sec"

  def Maximized_or_Minimized(self, event):
    if self.isMaximized():
      self.showNormal()
      self.label_5.setPixmap(QPixmap(self.dir_path+"/Icons/icons8-maximize-20.png"))
    else:
      self.showMaximized()
      self.label_5.setPixmap(QPixmap(self.dir_path+"/Icons/icons8-minimize20.png"))

  def Cat_Size(self, event):
    if self.Cat.width() == 150:
      self.Cat.setMaximumWidth(60)
      for i in self.Cat_label_list:
        i.setMaximumWidth(0)
        i.setMinimumWidth(0)
    else:
      self.Cat.setMaximumWidth(150)
      for i in self.Cat_label_list:
        i.setMaximumWidth(16777215)
        i.setMinimumWidth(90)
      
  def Move_Window(self , event):
    if not self.isMaximized():
      if event.buttons() == Qt.MouseButton.LeftButton:
        self.move(self.pos() + event.pos() - self.clickPostion)
        self.clickPostion = event.pos()
        event.accept()
  
  def active_cat(self , page):
    for x in self.Cat_list:
      x.setStyleSheet("background-color:#233647")
    page.setStyleSheet("background-color:#232800")

  def mousePressEvent(self, event) -> None:
    self.clickPostion = event.pos()
    

#######################################################################################33
  def battery(self):
    batt = psutil.sensors_battery()

    if not hasattr(psutil, "sensors_battery"):
      self.batt_status.setText("PlatForm Not Supported")
    
    if batt is None:
      self.batt_status.setText("No Battery Installed")
      return

    if batt.power_plugged:
      self.batt_charge.setText(str(round(batt.percent, 2))+"%")
      self.batt_timeLeft.setText("N/A")
      if batt.percent < 100:
        self.batt_status.setText("Charging")
      else:
        self.batt_status.setText("Fully Charged")
      
      self.batt_plug.setText("Yes")
    else:
      self.batt_charge.setText(str(round(batt.percent,2))+"%")
      self.batt_timeLeft.setText(self.sec2hour(batt.secsleft))
      if batt.percent < 100:
        self.batt_status.setText("DisCharging")
      else:
        self.batt_status.setText("Fully Charged")

      self.batt_plug.setText("No")
    
    self.batt_usage.setValue(batt.percent)

    self.batt_usage.setDataColors([(0., QColor.fromRgb(33, 150, 243))])
    self.batt_char.setStyleSheet("color:rgb(33, 150, 243)")

  def cpu_ram(self):
    totalRam = 1.0
    totalRam = psutil.virtual_memory()[0] * totalRam
    totalRam = round(totalRam / (1024**3) , 2)
    self.totalRam.setText(str(totalRam)+'GB')

    availRam = 1.0
    availRam = psutil.virtual_memory()[1] * availRam
    availRam = round(availRam / (1024**3) , 2)
    self.availRam.setText(str(availRam)+'GB')
    
    ramUsed = 1.0
    ramUsed = psutil.virtual_memory()[3] * ramUsed
    ramUsed = round(ramUsed / (1024**3) , 2)
    self.usedRam.setText(str(ramUsed)+'GB')

    freeRam = 1.0
    freeRam = psutil.virtual_memory()[4] * freeRam
    freeRam = round(freeRam / (1024**3) , 2)
    self.freeRam.setText(str(freeRam)+'GB')

    ramUsage = psutil.virtual_memory()[2]
    self.ramUsage.setText(str(ramUsage)+'%')
    self.bar_ram.setValue(ramUsage)
    if ramUsage < 60:
      self.bar_ram.setDataColors([(0., QColor.fromRgb(255, 150, 0))])
      self.chart_fram_2.setStyleSheet("color:rgb(255, 152, 0)")
    elif ramUsage < 90:
      self.bar_ram.setDataColors([(0., QColor.fromRgb(255, 87, 43))])
      self.chart_fram_2.setStyleSheet("color:rgb(255, 87, 43)")
    else:
      self.bar_ram.setDataColors([(0., QColor.fromRgb(233, 30, 99))])
      self.chart_fram_2.setStyleSheet("color:rgb(233, 30, 99)")

    core = psutil.cpu_count()
    self.cpu_count.setText(str(core))

    cpuPer = psutil.cpu_percent()
    self.cpu_per.setText(str(cpuPer) + "%")
    self.bar_cpu.setValue(cpuPer)
    if ramUsage < 60:
      self.bar_cpu.setDataColors([(0., QColor.fromRgb(255, 150, 0))])
      self.chart_fram_1.setStyleSheet("color:rgb(255, 152, 0)")
    elif ramUsage < 90:
      self.bar_cpu.setDataColors([(0., QColor.fromRgb(255, 87, 43))])
      self.chart_fram_1.setStyleSheet("color:rgb(255, 87, 43)")
    else:
      self.bar_cpu.setDataColors([(0., QColor.fromRgb(233, 30, 99))])
      self.chart_fram_1.setStyleSheet("color:rgb(233, 30, 99)")

    cpuMainCore = psutil.cpu_count(logical=False)
    self.mainCore.setText(str(cpuMainCore))

  def system_info(self):
    time = datetime.datetime.now().strftime("%I:%M:%S %p")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    self.sys_date.setText(str(date))
    self.sys_time.setText(str(time))

    self.sys_machine.setText(platform.machine())
    self.sys_ver.setText(platform.version())
    self.sys_plat.setText(platform.platform())
    self.sys_info.setText(platform.system())
    self.sys_proc.setText(platform.processor())

  def create_table_widget(self, rowPostion, columnPosition, text, tableName):
    qtablewidgetitem = QTableWidgetItem()
    getattr(self , tableName).setItem(rowPostion, columnPosition, qtablewidgetitem)
    getattr(self , tableName).item(rowPostion , columnPosition).setText(text)

  def Activities(self):
    for x in psutil.pids():
      rowPostion = self.tableWidget.rowCount()
      self.tableWidget.insertRow(rowPostion)

      try:
        process = psutil.Process(x)
        self.create_table_widget(rowPostion , 0, str(process.pid) , "tableWidget")
        self.create_table_widget(rowPostion , 1, str(process.name()) , "tableWidget")
        self.create_table_widget(rowPostion , 2, str(process.status()) , "tableWidget")
        self.create_table_widget(rowPostion, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')), "tableWidget")

        susben_btn = QPushButton(self.tableWidget)
        susben_btn.setText("Suspend")
        susben_btn.setStyleSheet("color:brown")
        self.tableWidget.setCellWidget(rowPostion , 4 , susben_btn)

        resume_btn = QPushButton(self.tableWidget)
        resume_btn.setText("Suspend")
        resume_btn.setStyleSheet("color:green")
        self.tableWidget.setCellWidget(rowPostion, 5, resume_btn)

        terminate_btn = QPushButton(self.tableWidget)
        terminate_btn.setText("Suspend")
        terminate_btn.setStyleSheet("color:orange")
        self.tableWidget.setCellWidget(rowPostion , 6 , terminate_btn)

        kill_btn = QPushButton(self.tableWidget)
        kill_btn.setText("Suspend")
        kill_btn.setStyleSheet("color:red")
        self.tableWidget.setCellWidget(rowPostion, 7, kill_btn)
      except:
        ...
    self.lineEdit.textChanged.connect(self.Find_Name)
  
  def Find_Name(self):
    name = self.lineEdit.text().lower()
    for row in range(self.tableWidget.rowCount()):
      item = self.tableWidget.item(row , 1)
      
      self.tableWidget.setRowHidden(row , name not in item.text().lower())

  def storage_Info(self):
    global platforms
    storage_dev = psutil.disk_partitions()
    for x in storage_dev:
      rowPostion = self.tableWidget_2.rowCount()
      self.tableWidget_2.insertRow(rowPostion)

      self.create_table_widget(rowPostion, 0, x.device, "tableWidget_2")
      self.create_table_widget(rowPostion, 1, x.mountpoint, "tableWidget_2")
      self.create_table_widget(rowPostion, 2, x.fstype, "tableWidget_2")
      self.create_table_widget(rowPostion, 3, x.opts, "tableWidget_2")

      if (sys.platform == 'linux') or (sys.platform == 'linux1') or (sys.platform == 'linux2'):
        self.create_table_widget(rowPostion, 4, str(x.maxfile), "tableWidget_2")
        self.create_table_widget(rowPostion, 5, str(x.maxpath), "tableWidget_2")
      else:
        self.create_table_widget(rowPostion, 4, "Function Not Avilable ON "+platforms[sys.platform], "tableWidget_2")
        self.create_table_widget(rowPostion, 5, "Function Not Avilable ON "+platforms[sys.platform], "tableWidget_2")
      try:
        disk_usage = shutil.disk_usage(fr"{x.mountpoint}")      

        self.create_table_widget(rowPostion, 6, str((disk_usage.total)/(1024**3))+' GB', "tableWidget_2")
        self.create_table_widget(rowPostion, 7, str((disk_usage.free)/(1024**3))+' GB', "tableWidget_2")
        self.create_table_widget(rowPostion, 8, str((disk_usage.used)/(1024**3))+' GB', "tableWidget_2")

        fulldisk = (disk_usage.used / disk_usage.total) * 100

        progressBar = QProgressBar(self.tableWidget_2.cellWidget(rowPostion , 9))
        progressBar.setObjectName("progressBar")
        progressBar.setValue(round(fulldisk))
        progressBar.setStyleSheet("color:#03A9F4")
        self.tableWidget_2.setCellWidget(rowPostion, 9, progressBar)
      except:
        self.create_table_widget(rowPostion, 6, "N/A", "tableWidget_2")
        self.create_table_widget(rowPostion, 7, "N/A", "tableWidget_2")
        self.create_table_widget(rowPostion, 8, "N/A", "tableWidget_2")

        progressBar = QProgressBar(self.tableWidget_2.cellWidget(rowPostion, 9))
        progressBar.setObjectName("progressBar")
        progressBar.setValue(0)
        progressBar.setStyleSheet("color:#03A9F4")
        progressBar.setEnabled(False)
        self.tableWidget_2.setCellWidget(rowPostion, 9, progressBar)

  def sensor_info(self):
    if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':
      for x in psutil.sensors_temperatures():
        for y in psutil.sensors_temperatures()[x]:
          rowPostion = self.tableWidget_3.rowCount()

          self.tableWidget_3.insertRow(rowPostion)

          self.create_table_widget(rowPostion, 0, x, 'tableWidget_3')
          self.create_table_widget(rowPostion, 1, y.label, 'tableWidget_3')
          self.create_table_widget(rowPostion, 2, str(y.current), 'tableWidget_3')
          self.create_table_widget(rowPostion, 3, str(y.high), 'tableWidget_3')
          self.create_table_widget(rowPostion, 4, str(y.critical), 'tableWidget_3')

          temp_per = (y.current / y.high) * 100

          progressBar = QProgressBar(self.tableWidget_3)
          progressBar.setObjectName("progressBar")
          progressBar.setValue(round(temp_per))
          progressBar.setStyleSheet("color:#03A9F4")
          self.tableWidget_3.setCellWidget(rowPostion, 5, progressBar)
    else:
      global platforms
      rowPostion = self.tableWidget_3.rowCount()
      self.tableWidget_3.insertRow(rowPostion)

      self.create_table_widget(rowPostion, 0,"Function Not Supported "+platforms[sys.platform], 'tableWidget_3')
      self.create_table_widget(rowPostion, 1,"N/A" , 'tableWidget_3')
      self.create_table_widget(rowPostion, 2,"N/A" , 'tableWidget_3')
      self.create_table_widget(rowPostion, 3,"N/A" , 'tableWidget_3')
      self.create_table_widget(rowPostion, 4,"N/A" , 'tableWidget_3')
      self.create_table_widget(rowPostion, 5,"N/A" , 'tableWidget_3')

  def network_info(self):
    for x in psutil.net_if_stats():
      z = psutil.net_if_stats()
      rowPostion = self.tableWidget_4.rowCount()
      self.tableWidget_4.insertRow(rowPostion)

      self.create_table_widget(rowPostion, 0, x, 'tableWidget_4')
      self.create_table_widget(rowPostion, 1, str(z[x].isup), 'tableWidget_4')
      self.create_table_widget(rowPostion, 2, str(z[x].duplex), 'tableWidget_4')
      self.create_table_widget(rowPostion, 3, str(z[x].speed), 'tableWidget_4')
      self.create_table_widget(rowPostion, 4, str(z[x].mtu), 'tableWidget_4')

    for x in psutil.net_io_counters(pernic=True):
      z = psutil.net_io_counters(pernic=True)
      rowPostion = self.tableWidget_5.rowCount()
      self.tableWidget_5.insertRow(rowPostion)

      self.create_table_widget(rowPostion, 0, x, 'tableWidget_5')
      self.create_table_widget(rowPostion, 1, str(z[x].bytes_sent), 'tableWidget_5')
      self.create_table_widget(rowPostion, 2, str(z[x].bytes_recv), 'tableWidget_5')
      self.create_table_widget(rowPostion, 3, str(z[x].packets_sent), 'tableWidget_5')
      self.create_table_widget(rowPostion, 4, str(z[x].packets_recv), 'tableWidget_5')
      self.create_table_widget(rowPostion, 5, str(z[x].errin), 'tableWidget_5')
      self.create_table_widget(rowPostion, 6, str(z[x].errout), 'tableWidget_5')
      self.create_table_widget(rowPostion, 7, str(z[x].dropin), 'tableWidget_5')
      self.create_table_widget(rowPostion, 8, str(z[x].dropout), 'tableWidget_5')

    for x in psutil.net_if_addrs():
      z = psutil.net_if_addrs()

      for y in z[x]:
        rowPostion = self.tableWidget_6.rowCount()
        self.tableWidget_6.insertRow(rowPostion)

        self.create_table_widget(rowPostion, 0, str(x), 'tableWidget_6')
        self.create_table_widget(rowPostion, 1, str(y.family), 'tableWidget_6')
        self.create_table_widget(rowPostion, 2, str(y.address), 'tableWidget_6')
        self.create_table_widget(rowPostion, 3, str(y.netmask), 'tableWidget_6')
        self.create_table_widget(rowPostion, 4, str(y.broadcast), 'tableWidget_6')
        self.create_table_widget(rowPostion, 5, str(y.ptp), 'tableWidget_6')

      for x in psutil.net_connections():
        z = psutil.net_connections()
        rowPostion = self.tableWidget_7.rowCount()
        self.tableWidget_7.insertRow(rowPostion)

        self.create_table_widget(rowPostion, 0, str(x.fd), 'tableWidget_7')
        self.create_table_widget(rowPostion, 1, str(x.family), 'tableWidget_7')
        self.create_table_widget(rowPostion, 2, str(x.type), 'tableWidget_7')
        self.create_table_widget(rowPostion, 3, str(x.laddr), 'tableWidget_7')
        self.create_table_widget(rowPostion, 4, str(x.raddr), 'tableWidget_7')
        self.create_table_widget(rowPostion, 5, str(x.status), 'tableWidget_7')
        self.create_table_widget(rowPostion, 6, str(x.pid), 'tableWidget_7')

###########################################################
  def finisher(self):
    self.cpu_ram()
    self.battery()
    self.system_info()
    self.Activities()
    self.storage_Info()
    self.sensor_info()
    self.network_info()


app = QApplication(sys.argv)
MainWindow = SystemMonitor()
MainWindow.show()
sys.exit(app.exec())

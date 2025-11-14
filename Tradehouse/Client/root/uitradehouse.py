import ui
import chat
import dbg
from _weakref import proxy
import snd
import net
import constInfo
import player
import localeInfo
import uiToolTip
import wndMgr
import mouseModule
import item
import time
import grp
import uiCommon
import tradehouse
import wndMgr
import snd
import ime
import app

LOCALIZATION = {
	"HISTORY" : "Elõzmények - Utolsó 50 eladás",
	"REFRESH" : "Frissít",
	"LOG_LINE" : "Eladva: %s (x%s) Ár: %s Rúd Dátum: %s",
	"BALANCE_MODIFY" : "Egyenleg módosítás",
	"BALANCE_GET" : "Egyenleg kivétel",
	"BALANCE_BTN" : "Alkalmaz",
	"BALANCE_ADD" : "Egyenleg hozzáadás",
	"ITEM_SELL_TITLE" : "Tárgy eladása",
	"ITEM_ADD_TEXT" : "Húzd bele a tárgyat!",
	"PRICE" : "Ár:",
	"SELL" : "Eladni",
	"ITEM_NAME" : "%s (x%d)",
	"ITEM_PRICE" : "Ár: %d Rúd (darabja: %d)",
	"EXPIRE" : "Lejárat: %s",
	"ITEM_DETAIL" : "%s (%d darab)",
	"SHOW_TEXT" : "Megjelenítve az oldalon: %d",
	"BALANCE" : "Egyenleg: %d Rúd",
	"SEARCH_TEXT" : "Keresõ.. (min 4 karakter)",
	"BACK" : "Elõzõ",
	"NEXT" : "Következõ",
	"SELECT_CATEGORY" : "Válassz kategóriát:",
	"HISTORY_LABEL" : "Elõzmények:",
	"HISTORY_BTN" : "Eladások megny.",
	"ORDER1" : "Olcsók elõl",
	"ORDER2" : "Drágák elõl",
	"SEARCH" : "Keresés",
	"ADMIN" : "Adminisztráció:",
	"NULL_BALANCE" : "Egyenleg: 0 Rúd",
	"BALANCE_FILL" : "Egyenleg feltöltés",
	"STORAGE" : "Saját tárgyak",
}

CATEGORY_SYSTEM = [

##	{"Kategória név", itemType, SubType},

	{"NAME" : "Fegyverek: Kardok", "TYPE" : 1, "SUBTYPE" : 0},
	{"NAME" : "Fegyverek: Kétkezesek", "TYPE" : 1, "SUBTYPE" : 1},
	{"NAME" : "Fegyverek: Tõrök", "TYPE" : 1, "SUBTYPE" : 2},
	{"NAME" : "Fegyverek: Íjak", "TYPE" : 1, "SUBTYPE" : 3},
	{"NAME" : "Fegyverek: Legyezõk", "TYPE" : 1, "SUBTYPE" : 4},
	{"NAME" : "Fegyverek: Harangok", "TYPE" : 1, "SUBTYPE" : 5},
	
	{"NAME" : "Vértek", "TYPE" : 2, "SUBTYPE" : 0},
	{"NAME" : "Ékszerek: Sisakok", "TYPE" : 2, "SUBTYPE" : 1},
	{"NAME" : "Ékszerek: Pajzsok", "TYPE" : 2, "SUBTYPE" : 2},
	{"NAME" : "Ékszerek: Karkötõk", "TYPE" : 2, "SUBTYPE" : 3},
	{"NAME" : "Ékszerek: Cipõk", "TYPE" : 2, "SUBTYPE" : 4},
	{"NAME" : "Ékszerek: Nyakláncok", "TYPE" : 2, "SUBTYPE" : 5},
	
	{"NAME" : "Kosztümök: Vért", "TYPE" : 28, "SUBTYPE" : 0},
	{"NAME" : "Kosztümök: Fegyver", "TYPE" : 28, "SUBTYPE" : 2},
	{"NAME" : "Kosztümök: Haj", "TYPE" : 28, "SUBTYPE" : 1},
	{"NAME" : "Kosztümök: Pánt", "TYPE" : 28, "SUBTYPE" : 3},
	{"NAME" : "Kosztümök: Hátas", "TYPE" : 28, "SUBTYPE" : 4},
]

class HistoryBoard(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(400, 200)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName(LOCALIZATION["HISTORY"])
		self.Board.SetCloseEvent(self.Close)
		self.Board.Show()

		self.RefreshBtn = ui.Button()
		self.RefreshBtn.SetParent(self.Board)
		self.RefreshBtn.SetPosition(400 - 42 - 30, 7)
		self.RefreshBtn.SetSize(42,21)
		self.RefreshBtn.SetText(LOCALIZATION["REFRESH"])
		self.RefreshBtn.SetEvent(self.Refresh)
		self.RefreshBtn.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		self.RefreshBtn.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		self.RefreshBtn.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		self.RefreshBtn.Show()

		(self.bar, self.listbox) = self.ListBoxEx(self.Board, 8, 30, 382, 200 - 40)	
		
				
	def AddItem(self, d1, d2, d3, d4, d5):
		item.SelectItem(int(d2))
		self.listbox.AppendItem(ItemNoRender(LOCALIZATION["LOG_LINE"] % (item.GetItemName(), d4, d3, d5)))
		
	def Open(self):
		self.listbox.RemoveAllItems()
		self.Show()
		self.Board.Show()
		self.SetTop()

	def Close(self):
		self.Board.Hide()
		self.Hide()

	def Refresh(self):
		self.listbox.RemoveAllItems()
		net.SendChatPacket("/tradehouse history")

	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()	
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.SetViewItemCount(8)
		ListBox.Show()
		scroll = ui.ThinScrollBar()
		scroll.SetParent(bar)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return (bar, ListBox)
		

class MoneyBoard(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()
		self.ServerCommand = ""

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(200, 150)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName(LOCALIZATION["BALANCE_MODIFY"])
		self.Board.SetCloseEvent(self.Close)
		self.Board.Show()

		self.BalanceBoard = ui.ThinBoardCircle()
		self.BalanceBoard.SetParent(self.Board)
		self.BalanceBoard.SetSize(130, 20)
		self.BalanceBoard.SetPosition(200/2 - 130/2, 34)
		self.BalanceBoard.Show()

		self.BalanceText = ui.TextLine()
		self.BalanceText.SetParent(self.BalanceBoard)
		self.BalanceText.SetPosition(0,0)
		self.BalanceText.SetText(LOCALIZATION["BALANCE_GET"])			
		self.BalanceText.SetVerticalAlignCenter()
		self.BalanceText.SetHorizontalAlignCenter()
		self.BalanceText.SetWindowVerticalAlignCenter()
		self.BalanceText.SetWindowHorizontalAlignCenter()		
		self.BalanceText.Show()

		(self.search_bar, self.search_ListBox) = self.EditLine(self.Board, "0", 200/2 - 130/2, 34+38, 130, 20, 10)

		self.SellItemButton = ui.Button()
		self.SellItemButton.SetParent(self.Board)
		self.SellItemButton.SetPosition(60, 110)
		self.SellItemButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.SellItemButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.SellItemButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.SellItemButton.SetText(LOCALIZATION["BALANCE_BTN"])		
		self.SellItemButton.SetEvent(self.SellItem)
		self.SellItemButton.Show()

	def UpdateText(self, num):
		if num == 0:
			self.BalanceText.SetText(LOCALIZATION["BALANCE_GET"])
			self.ServerCommand = "/tradehouse get_balance "
		else:
			self.BalanceText.SetText(LOCALIZATION["BALANCE_ADD"])	
			self.ServerCommand = "/tradehouse add_balance "
			
	def SellItem(self):
		net.SendChatPacket(self.ServerCommand + self.search_ListBox.GetText())

	def Open(self):
		self.Show()
		self.Board.Show()
		self.SetTop()

	def Close(self):
		self.Board.Hide()
		self.Hide()

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.ThinBoardCircle()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(5, 5)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetText(editlineText)
		Value.SetNumberMode()
		Value.Show()
		return SlotBar, Value

class SpecialBoard(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()
		self.Slot = -1
		self.Vnum = 0

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(196, 150)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName(LOCALIZATION["ITEM_SELL_TITLE"])
		self.Board.SetCloseEvent(self.Close)
		self.Board.Show()

		self.itemSlotWindow = ui.GridSlotWindow()
		self.itemSlotWindow.SetParent(self.Board)
		self.itemSlotWindow.SetPosition(10, 34)
		self.itemSlotWindow.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
		self.itemSlotWindow.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.itemSlotWindow.Show()	
		
		# self.itemSlotWindow.SetItemSlot(0, 19, 1)
		# self.itemSlotWindow.RefreshSlot()	

		self.itemSlotWindow.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.BalanceBoard = ui.ThinBoardCircle()
		self.BalanceBoard.SetParent(self.Board)
		self.BalanceBoard.SetSize(130, 20)
		self.BalanceBoard.SetPosition(34 + 15, 34)
		self.BalanceBoard.Show()

		self.BalanceText = ui.TextLine()
		self.BalanceText.SetParent(self.BalanceBoard)
		self.BalanceText.SetPosition(0,0)
		self.BalanceText.SetText(LOCALIZATION["ITEM_ADD_TEXT"])			
		self.BalanceText.SetVerticalAlignCenter()
		self.BalanceText.SetHorizontalAlignCenter()
		self.BalanceText.SetWindowVerticalAlignCenter()
		self.BalanceText.SetWindowHorizontalAlignCenter()		
		self.BalanceText.Show()

		self.SellPriceText = ui.TextLine()
		self.SellPriceText.SetParent(self.Board)
		self.SellPriceText.SetPosition(34 + 15, 34+40)
		self.SellPriceText.SetFontName("Arial:15")	
		self.SellPriceText.SetText(LOCALIZATION["PRICE"])		
		self.SellPriceText.Show()	

		(self.search_bar, self.search_ListBox) = self.EditLine(self.Board, "0", 34 + 15 + 20, 34+38, 100, 20, 10)

		self.SellItemButton = ui.Button()
		self.SellItemButton.SetParent(self.Board)
		self.SellItemButton.SetPosition(60, 110)
		self.SellItemButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.SellItemButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.SellItemButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.SellItemButton.SetText(LOCALIZATION["SELL"])		
		self.SellItemButton.SetEvent(self.SellItem)
		self.SellItemButton.Show()

	def SellItem(self):
		net.SendChatPacket("/tradehouse add %d %s" % (self.Slot, self.search_ListBox.GetText()))

	def OnUpdate(self):
		itemVNum = player.GetItemIndex(player.SLOT_TYPE_INVENTORY, self.Slot)
		
		if itemVNum != self.Vnum:
			self.Slot = -1	
			self.Vnum = itemVNum
			self.itemSlotWindow.SetItemSlot(0, 0, 0)
			self.itemSlotWindow.RefreshSlot()			

	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			self.Vnum = itemVNum
			self.Slot = attachedSlotPos
			self.itemSlotWindow.SetItemSlot(0, itemVNum, 1)
			self.itemSlotWindow.RefreshSlot()				

	def UnselectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		self.Slot = -1	
		self.Vnum = 0
		self.itemSlotWindow.SetItemSlot(0, 0, 0)
		self.itemSlotWindow.RefreshSlot()			

	def Open(self):
		self.Show()
		self.Board.Show()
		self.SetTop()

	def Close(self):
		self.Board.Hide()
		self.Hide()

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.ThinBoardCircle()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(5, 5)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetText(editlineText)
		Value.SetNumberMode()
		Value.Show()
		return SlotBar, Value

class SearchWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Selected = 0
		self.interface = None
		#self.CreateBoard()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)			
		
	def CreateBoard(self, parent, realParent, x, y):
		self.interface = realParent
		self.SearchBoard = ui.ThinBoardCircle()
		self.SearchBoard.SetParent(parent)
		self.SearchBoard.SetSize(170, 100)
		self.SearchBoard.SetPosition(x, y)

		(self.bar, self.listbox) = self.ListBoxEx(self.SearchBoard, 5, 2, 160, 96)	
		self.listbox.RemoveAllItems()
		#self.listbox.AppendItem(Item("Fegyverek: Kardok"))
		self.listbox.SetSelectEvent(ui.__mem_func__(self.OnSelectItem))

	def OnSelectItem(self):
		item = self.listbox.GetSelectedItem()
		self.interface.UpdateSelectedVnum(item.GetIndex(), item.GetText())
		self.Close()
		
	def Close(self):
		self.SearchBoard.Hide()
		self.Hide()		

	def Open(self):		
		self.Show()
		self.SearchBoard.Show()
		self.SetTop()
		self.listbox.RemoveAllItems()

	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()	
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.SetViewItemCount(5)
		ListBox.Show()
		scroll = ui.ThinScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return (bar, ListBox)
		
	def Update(self, text):
		# if app.GetGlobalTime() - self.lastUpdateSearching > 500:
			# self.lastUpdateSearching = app.GetGlobalTime()
		
		self.interface.UpdateSelectedVnum(0, "")
		
		if len(text) < 4:
			if self.IsShow():
				self.Close()
			return
		else:
			if not self.IsShow():
				self.Open()
			
		self.listbox.RemoveAllItems()
		vnum_list = tradehouse.SearchItem(text)
		
		for vnum in vnum_list:
			item.SelectItem(vnum)
			self.listbox.AppendItem(Item(item.GetItemName(), vnum))
			#self.listbox.AppendItem(item.GetItemName())
		
class ItemCard(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Vnum = 0
		self.Count = 0
		self.OwnerFlag = 0
		self.Expire = 0
		self.Unique = 0
		self.interface = 0
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)			
		
	def BindInterface(self, mem):
		self.interface = mem
		
	def Update(self, unique = 0, vnum = 0, count = 0, price = 0, ownerflag = 0, owner="", expire=0):
		self.OwnerFlag = ownerflag
		self.Vnum = vnum
		self.Unique = unique
		
		if vnum == 0:
			self.SetEmpty()
			return
		item.SelectItem(vnum)
		self.SellerName.SetText(owner)
		self.Expire = expire
		self.ItemName.SetText(LOCALIZATION["ITEM_NAME"] % (item.GetItemName(), count))
		self.PriceText.SetText(LOCALIZATION["ITEM_PRICE"] % (price, price/count))
		self.itemSlotWindow.SetItemSlot(0, vnum, count)
		self.itemSlotWindow.RefreshSlot()


		if ownerflag == 0:
			self.BuyButton.SetUpVisual("tradehouse/buy1.tga")
			self.BuyButton.SetOverVisual("tradehouse/buy2.tga")
			self.BuyButton.SetDownVisual("tradehouse/buy3.tga")
		else:
			self.BuyButton.SetUpVisual("tradehouse/return1.tga")
			self.BuyButton.SetOverVisual("tradehouse/return2.tga")
			self.BuyButton.SetDownVisual("tradehouse/return3.tga")			
			
		self.BuyButton.Show()
		
	def SetEmpty(self):
		self.ItemName.SetText("")
		self.PriceText.SetText("")
		self.SellerName.SetText("")
		self.ExpireTime.SetText("")
		self.itemSlotWindow.SetItemSlot(0, 0, 0)
		self.itemSlotWindow.RefreshSlot()	
		self.BuyButton.Hide()		
	
	
	
	def SendEvent(self):
		if self.OwnerFlag == 0:
			net.SendChatPacket("/tradehouse buy %d" % self.Unique)
		else:
			net.SendChatPacket("/tradehouse get %d" % self.Unique)
	
	
	def OnUpdate(self):
		if self.Vnum != 0:
			self.ExpireTime.SetText(LOCALIZATION["EXPIRE"] % localeInfo.PrivateShopSecondToDHMS(max(0, self.Expire - app.GetGlobalTimeStamp())))
	
	def Create(self, parent, index, vnum = 19, count = 2, price = 100):
		self.Vnum = vnum
		self.Count = count
		
		self.board = ui.ThinBoardCircle()
		self.board.SetParent(parent)
		self.board.SetSize(200, 100)
		self.board.SetPosition(3, 3 + (102 * index))
		self.board.Show()
		
		self.itemSlotWindow = ui.GridSlotWindow()
		self.itemSlotWindow.SetParent(self.board)
		self.itemSlotWindow.SetPosition(3, 2)
		self.itemSlotWindow.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
		self.itemSlotWindow.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.itemSlotWindow.Show()	
		
		self.itemSlotWindow.SetItemSlot(0, vnum, count)
		self.itemSlotWindow.RefreshSlot()		

		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		

		item.SelectItem(vnum)

		self.ItemName = ui.TextLine()
		self.ItemName.SetParent(self.board)
		self.ItemName.SetPosition(42,6)
		self.ItemName.SetFontName("Arial:15")
		self.ItemName.SetText(LOCALIZATION["ITEM_DETAIL"] % (item.GetItemName(), count))
		self.ItemName.Show()

		self.SellerName = ui.TextLine()
		self.SellerName.SetParent(self.board)
		self.SellerName.SetPosition(42,30)
		self.SellerName.SetFontName("Arial:15")
		self.SellerName.SetText("")
		self.SellerName.Show()

		self.ExpireTime = ui.TextLine()
		self.ExpireTime.SetParent(self.board)
		self.ExpireTime.SetPosition(42,55)
		self.ExpireTime.SetFontName("Arial:14")
		self.ExpireTime.SetText("")
		self.ExpireTime.Show()
		
		self.PriceText = ui.TextLine()
		self.PriceText.SetParent(self.board)
		self.PriceText.SetPosition(42,77)
		self.PriceText.SetFontName("Arial:14")
		self.PriceText.SetPackedFontColor(0xffFFFF33)
		self.PriceText.SetText(LOCALIZATION["ITEM_PRICE"] % (price, price/count))
		self.PriceText.Show()		

		self.BuyButton = ui.Button()
		self.BuyButton.SetParent(self.board)
		self.BuyButton.SetPosition(200-35,3)	
		self.BuyButton.SetEvent(self.Action)
		self.BuyButton.SetUpVisual("tradehouse/buy1.tga")
		self.BuyButton.SetOverVisual("tradehouse/buy2.tga")
		self.BuyButton.SetDownVisual("tradehouse/buy3.tga")
		self.BuyButton.Show()


	def OverInItem(self, slotIndex):
		self.interface.ShowToolTip(self.Unique)

	def OverOutItem(self):
		self.interface.HideToolTip()

	def Action(self):
		if self.OwnerFlag == 0:
			net.SendChatPacket("/tradehouse buy %d" % self.Unique)
		else:
			net.SendChatPacket("/tradehouse get %d" % self.Unique)

class TradeHouse(ui.ScriptWindow):			
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.SearchWnd = SearchWindow()
		self.Initialize()
		self.Init()

	def Initialize(self):
		tradehouse.SetHandler(self)
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.HideToolTip()
		
		self.interface = None
	
		self.SelectedVnum = 0
		self.AddItemBoard = 0
		self.MoneyBoard = 0
		self.HistoryBoard = 0
		self.Items = []
		
		self.LoadString = ""
		
		self.Offset = 0
		self.Category = 1
		self.SubCategory = 0
		self.AscLoading = 1
		self.OwnerFlag = 0

	def UpdateOffset(self, num):
		self.Offset = self.Offset + (num*20)

		if self.Offset < 0:
			self.Offset = 0

		self.LoadItems()

	def AppendHistory(self, s1, s2, s3, s4, s5):
		self.HistoryBoard.AddItem(s1,s2,s3,s4,s5)

	def LoadItems(self):
		self.scrollBar.SetPos(0)
		
		if self.OwnerFlag == 1:
			self.LoadStorage()
			return
		
		self.LoadString = "/tradehouse show "
		self.LoadString += str(self.Category) + " "
		self.LoadString += str(self.SubCategory) + " "
		self.LoadString += str(self.Offset) + " "
		self.LoadString += str(self.AscLoading) + " "
		self.LoadString += str(self.SelectedVnum)
	
		net.SendChatPacket(self.LoadString)

	def LoadStorage(self):
		self.LoadString = "/tradehouse storage "
		self.LoadString += str(self.Offset)
		
		net.SendChatPacket(self.LoadString)		

	def OnUpdate(self):
		for x in range(len(self.ItemCards)):
			self.ItemCards[x].OnUpdate()

	def ShowToolTip(self, unique):
		vnum = tradehouse.GetInfo(unique, -1) ## vnum
		attrs = tradehouse.GetInfo(unique, 0) ## attrs
		sockets = tradehouse.GetInfo(unique, 1) ## sockets
	
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.AddItemData(vnum, sockets, attrs)
		self.tooltipItem.ShowToolTip()
		
	def HideToolTip(self):
		self.tooltipItem.HideToolTip()

	def GetOwnerFlag(self):
		return self.OwnerFlag

	def Refresh(self):
		self.LoadItems()

	def UpdateResultBoard(self, num, ownerflag):

		self.ResultText.SetText(LOCALIZATION["SHOW_TEXT"] % (num))
		
		self.OwnerFlag = ownerflag
		
		if num == 0: ## Ha üres lenne az oldal, 
			self.Offset = 0
			return
		
		if num < 20: ## Ha nem teljes az oldal, akkor biztos nincs következõ.
			self.NextButton.Down()
			self.NextButton.Disable()
		else:
			self.NextButton.SetUp()
			self.NextButton.Enable()			
		
	
	def UpdateBalance(self, num):
		self.BalanceText.SetText(LOCALIZATION["BALANCE"] % num)			
		
	def LoadItemsNew(self):
		self.Offset = 0
		self.OwnerFlag = 0
		self.LoadItems()

	def Destroy(self):
		self.Close()
		self.Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Initialize()	

	def UpdateSelectedVnum(self, vnum, text, forceUpdate = True):
		self.SelectedVnum = vnum
		if vnum != 0:
			self.AcceptIcon.Show()
		else:
			self.AcceptIcon.Hide()
			
		if text != "":
			self.search_ListBox.SetText(text)	
			
		if vnum != 0:
			item.SelectItem(vnum)
			self.Category = item.GetItemType()
			self.SubCategory = item.GetItemSubType()		
		# else:
			# self.Category = 0
			# self.SubCategory = 0
		
		if forceUpdate:
			self.listbox.SelectIndex(-1)
		else:
			self.search_ListBox.SetText(LOCALIZATION["SEARCH_TEXT"])

	def Init(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "tradehouse_ui.py")
		except:
			import exception
			exception.Abort("TradeHouse.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.item_board = self.GetChild("item_board")
			self.main_board = self.GetChild("main_board")
			self.ResultText = self.GetChild("ResultText")
			self.ResultText.SetText("")
			
			self.ItemCards = []
			self.ItemCards.append(ItemCard())
			self.ItemCards.append(ItemCard())
			self.ItemCards.append(ItemCard())
			self.ItemCards.append(ItemCard())
			
			for x in range(4):
				self.ItemCards[x].BindInterface(self)
				self.ItemCards[x].Create(self.item_board, x)

			scrollBar = ui.ScrollBar()
			scrollBar.SetParent(self.item_board)
			scrollBar.SetScrollBarSize(4*100)
			scrollBar.SetPosition(208,8)
			scrollBar.SetMiddleBarSize(10.0 / 20.0)
			scrollBar.SetScrollEvent(self.__OnScroll)
			
			self.scrollBar = scrollBar
			self.scrollBar.SetPos(0)
			self.scrollBar.Show()

			self.BackButton = ui.Button()
			self.BackButton.SetParent(self.item_board)
			self.BackButton.SetPosition(20, 415)	
			self.BackButton.SetEvent(lambda : self.UpdateOffset(-1))
			self.BackButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.BackButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.BackButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.BackButton.SetText(LOCALIZATION["BACK"])		
			self.BackButton.Show()

			self.NextButton = ui.Button()
			self.NextButton.SetParent(self.item_board)
			self.NextButton.SetPosition(120, 415)	
			self.NextButton.SetEvent(lambda : self.UpdateOffset(1))
			self.NextButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.NextButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.NextButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.NextButton.SetText(LOCALIZATION["NEXT"])		
			self.NextButton.Show()

			(self.search_bar, self.search_ListBox) = self.EditLine(self.main_board, LOCALIZATION["SEARCH_TEXT"], 8, 10, 170, 25, 25)
			(self.bar, self.listbox) = self.ListBoxEx(self.main_board, 8, 55+5, 172, 205)			

			self.AcceptIcon = ui.ImageBox()
			self.AcceptIcon.SetParent(self.main_board)
			self.AcceptIcon.SetPosition(8 + 170 - 25, 12)
			self.AcceptIcon.LoadImage("tradehouse/accept.tga")
			self.AcceptIcon.Hide()
						
			self.CategoryText = ui.TextLine()
			self.CategoryText.SetParent(self.main_board)
			self.CategoryText.SetPosition(10,40)
			self.CategoryText.SetText(LOCALIZATION["SELECT_CATEGORY"])
			self.CategoryText.Show()

			self.search_ListBox.SetSearchBoard(self.SearchWnd)
			self.SearchWnd.CreateBoard(self.main_board, self, 8, 10 + 25 - 1)

			self.SalesText = ui.TextLine()
			self.SalesText.SetParent(self.main_board)
			self.SalesText.SetPosition(10,386+5-80+35)
			self.SalesText.SetText(LOCALIZATION["HISTORY_LABEL"])
			self.SalesText.Show()

			self.SalesOpen = ui.Button()
			self.SalesOpen.SetParent(self.main_board)
			#self.SalesOpen.SetPosition(5, 46 + 215+25+35)	
			self.SalesOpen.SetPosition(5, 386 + 15+5-75+35)
			self.SalesOpen.SetEvent(self.OpenHistoryDialog)
			self.SalesOpen.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.SalesOpen.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.SalesOpen.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.SalesOpen.SetText(LOCALIZATION["HISTORY_BTN"])		
			self.SalesOpen.Show()

			self.OrderCheap = ui.RadioButton()
			self.OrderCheap.SetParent(self.main_board)
			self.OrderCheap.SetPosition(5, 386 + 15+5-75-62)	
			self.OrderCheap.SetEvent(lambda: self.UpdateAsc(0))
			self.OrderCheap.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.OrderCheap.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.OrderCheap.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.OrderCheap.SetText(LOCALIZATION["ORDER1"])		
			self.OrderCheap.Show()

			self.OrderExpensive = ui.RadioButton()
			self.OrderExpensive.SetParent(self.main_board)
			self.OrderExpensive.SetPosition(98, 386 + 15+5-75-62)	
			self.OrderExpensive.SetEvent(lambda: self.UpdateAsc(1))
			self.OrderExpensive.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.OrderExpensive.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.OrderExpensive.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.OrderExpensive.SetText(LOCALIZATION["ORDER2"])		
			self.OrderExpensive.Show()
	
			##d:/ymir work/ui/public/xlarge_button_01.sub

			self.SearchButton = ui.Button()
			self.SearchButton.SetParent(self.main_board)
			self.SearchButton.SetPosition(5, 386 + 15+5-75-32)	
			self.SearchButton.SetEvent(self.LoadItemsNew)
			self.SearchButton.SetUpVisual("d:/ymir work/ui/public/xlarge_button_01.sub")
			self.SearchButton.SetOverVisual("d:/ymir work/ui/public/xlarge_button_02.sub")
			self.SearchButton.SetDownVisual("d:/ymir work/ui/public/xlarge_button_03.sub")
			self.SearchButton.SetText(LOCALIZATION["SEARCH"])		
			self.SearchButton.Show()
	
			self.ControlText = ui.TextLine()
			self.ControlText.SetParent(self.main_board)
			self.ControlText.SetPosition(10,355+35)
			self.ControlText.SetText(LOCALIZATION["ADMIN"])
			self.ControlText.Show()

			self.BalanceBoard = ui.ThinBoardCircle()
			self.BalanceBoard.SetParent(self.main_board)
			self.BalanceBoard.SetSize(170, 20)
			self.BalanceBoard.SetPosition(8, 355 + 20+35)
			self.BalanceBoard.Show()

			self.BalanceText = ui.TextLine()
			self.BalanceText.SetParent(self.BalanceBoard)
			self.BalanceText.SetPosition(0,0)
			self.BalanceText.SetText(LOCALIZATION["NULL_BALANCE"])			
			self.BalanceText.SetVerticalAlignCenter()
			self.BalanceText.SetHorizontalAlignCenter()
			self.BalanceText.SetWindowVerticalAlignCenter()
			self.BalanceText.SetWindowHorizontalAlignCenter()		
			self.BalanceText.Show()

			self.BalanceGet = ui.Button()
			self.BalanceGet.SetParent(self.main_board)
			self.BalanceGet.SetPosition(5, 355 + 20+25+35)	
			self.BalanceGet.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.BalanceGet.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.BalanceGet.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.BalanceGet.SetText(LOCALIZATION["BALANCE_GET"])		
			self.BalanceGet.SetEvent(lambda : self.OpenMoneyDialog(0))
			self.BalanceGet.Show()

			self.BalanceUpload = ui.Button()
			self.BalanceUpload.SetParent(self.main_board)
			self.BalanceUpload.SetPosition(98, 355 + 20+25+35)	
			self.BalanceUpload.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.BalanceUpload.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.BalanceUpload.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.BalanceUpload.SetText(LOCALIZATION["BALANCE_FILL"])			
			self.BalanceUpload.SetEvent(lambda : self.OpenMoneyDialog(1))		
			self.BalanceUpload.Show()

			self.SellItem = ui.Button()
			self.SellItem.SetParent(self.main_board)
			self.SellItem.SetPosition(5, 355 + 20+25+25+35)	
			self.SellItem.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.SellItem.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.SellItem.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.SellItem.SetText(LOCALIZATION["ITEM_SELL_TITLE"])		
			self.SellItem.SetEvent(self.OpenAddItemDialog)
			self.SellItem.Show()

			self.MyItems = ui.Button()
			self.MyItems.SetParent(self.main_board)
			self.MyItems.SetPosition(98, 355 + 20+25+25+35)	
			self.MyItems.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.MyItems.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.MyItems.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.MyItems.SetText(LOCALIZATION["STORAGE"])		
			self.MyItems.SetEvent(self.LoadStorageMain)
			self.MyItems.Show()

			self.listbox.RemoveAllItems()
			self.listbox.SetSelectEvent(ui.__mem_func__(self.OnSelectItem_ListBox))
			
			for category in CATEGORY_SYSTEM:
				self.listbox.AppendItem(Item(category["NAME"], CATEGORY_SYSTEM.index(category)))

			self.UpdateAsc(0)
			
		except:
			import exception
			dbg.TraceError(exception.GetExceptionString("TradeHouse.LoadDialog.LoadScript"))

	def LoadStorageMain(self):
		self.Offset = 0
		self.LoadStorage()

	def OnSelectItem_ListBox(self):
		item = self.listbox.GetSelectedItem()

		self.Category = CATEGORY_SYSTEM[item.GetIndex()]["TYPE"]
		self.SubCategory = CATEGORY_SYSTEM[item.GetIndex()]["SUBTYPE"]	
		
		self.UpdateSelectedVnum(0, "", False)
	
	def ClearItems(self):
		self.Items = []
		
		for i in xrange(4):
			self.ItemCards[i].Update(0,0,0,0)
	
	def UpdateAsc(self, num):
		if num == 0:
			self.OrderCheap.Down()
			self.OrderExpensive.SetUp()
			self.AscLoading = 1
		else:
			self.OrderCheap.SetUp()
			self.OrderExpensive.Down()
			self.AscLoading = 0			
			
	
	def AddItemData(self, unique, vnum, count, price, expire, owner):
		#chat.AppendChat(0, "From binary %d %d %d %d Count %d" % (unique,vnum,count,price,tradehouse.GetCount()))
		self.scrollBar.SetMiddleBarSize(4.0 / float(tradehouse.GetCount()))
		
		if tradehouse.GetCount() < 4:
			self.scrollBar.Hide()
		else:
			self.scrollBar.Show()
		
		data = {
			"UNIQUE" : int(unique),
			"VNUM" : int(vnum),
			"PRICE" : int(price),
			"COUNT" : int(count),
			"OWNER" : "(" + owner + ")",
			"EXPIRE" : expire,
		}
		
		self.Items.append(data)
		
		self.__OnScroll()
		
	def TestFunc(self, val):
		chat.AppendChat(0, "From binary %d" % val)
	
	def __OnScroll(self):
		try:
			board_count = 4
			pos = int(self.scrollBar.GetPos() * (tradehouse.GetCount() - board_count))
			
			for i in xrange(board_count):
				realPos = i + pos
				self.ItemCards[i].Update(self.Items[realPos]["UNIQUE"], self.Items[realPos]["VNUM"],self.Items[realPos]["COUNT"],self.Items[realPos]["PRICE"], self.OwnerFlag, self.Items[realPos]["OWNER"], self.Items[realPos]["EXPIRE"])
		except:
			pass
			
	def OpenAddItemDialog(self):
		if not self.AddItemBoard:
			self.AddItemBoard = SpecialBoard()
			
		self.AddItemBoard.Open()
	
	def OpenMoneyDialog(self, num):
		if not self.MoneyBoard:
			self.MoneyBoard = MoneyBoard()
			
		self.MoneyBoard.UpdateText(num)
		self.MoneyBoard.Open()
	
	def OpenHistoryDialog(self):
		if not self.HistoryBoard:
			self.HistoryBoard = HistoryBoard()

		self.HistoryBoard.Open()	
	
	
	
	def Close(self):
		self.Hide()			
				
	def Open(self):	
	
		if len(self.Items) == 0:
			self.LoadItems()
			
		self.Show()
		self.SetTop()
		
	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()	
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.SetViewItemCount(10)
		ListBox.Show()
		scroll = ui.ThinScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return (bar, ListBox)

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.ThinBoardCircle()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = SpecialEditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(5, 5)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		#Value.SetMultiLine()
		Value.SetText(editlineText)
		#Value.OnIMEUpdate = self.SearchUpdate
		# Value.SetPlaceHolder(editlineText)
		# Value.SetPlaceHolderColor(0xffFFFF33)
		Value.Show()
		return SlotBar, Value


class SpecialEditLine(ui.EditLine):
	def __init__(self):
		ui.EditLine.__init__(self)
		self.eventReturn = 0
		self.eventEscape = 0
		self.SearchBoard = None
		
	def SetSearchBoard(self, board):
		self.SearchBoard = board
		
	def __del__(self):
		ui.EditLine.__del__(self)

	def SetReturnEvent(self, event):
		self.eventReturn = event

	def SetEscapeEvent(self, event):
		self.eventEscape = event

	def OnIMEReturn(self):
		text = self.GetText()

		if len(text) > 0:
			self.eventReturn(text)

		else:
			wndMgr.KillFocus()
			self.eventEscape()

		self.SetText("")
		return TRUE

	def OnPressEscapeKey(self):
		self.SetText(LOCALIZATION["SEARCH_TEXT"])
		self.SearchBoard.Update("")
		wndMgr.KillFocus()
		self.eventEscape()
		return TRUE

	def OnKillFocus(self):
		self.SearchBoard.Close()
		if len(self.GetText()) == 0:
			self.SetText(LOCALIZATION["SEARCH_TEXT"])
			self.SearchBoard.Update("")
			
		self.SetText(ime.GetText(self.bCodePage))
		self.OnIMECloseCandidateList()
		self.OnIMECloseReadingWnd()
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)		

	def OnSetFocus(self):
		#self.SearchBoard.Open()
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)
		if self.numberMode:
			ime.SetNumberMode()
		else:
			ime.SetStringMode()
		ime.EnableCaptureInput()
		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()
		wndMgr.ShowCursor(self.hWnd, True)

	def OnKeyDown(self, key):
		self.SearchBoard.Update(self.GetText())
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False
		if app.DIK_V == key:
			if app.IsPressed(app.DIK_LCONTROL):
				ime.PasteTextFromClipBoard()

		return True

	def OnMouseLeftButtonDown(self):
		self.SetText("")	
		self.SearchBoard.Update(self.GetText())
		if False == self.IsIn():
			#self.SetText("Keresõ.. (min 4 karakter)")	
			return False

		self.SetFocus()
		ime.SetCursorPosition(0)

class Item(ui.ListBoxEx.Item):
	def __init__(self, fileName, index = 0):
		ui.ListBoxEx.Item.__init__(self)
		self.canLoad=0
		self.text=fileName
		self.index = index
		self.textLine=self.__CreateTextLine(fileName)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.text

	def GetIndex(self):
		return self.index

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)

		textLine.SetPosition(4, 0)

		textLine.SetText(fileName)
		textLine.Show()
		return textLine

	def OnSelectedRender(self):
		x, y = self.GetGlobalPosition()
		grp.SetColor(grp.GenerateColor(80*255, 181*255, 43*255, 0.7))
		grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())
		
		#chat.AppendChat(0, "asd")


class ItemNoRender(ui.ListBoxEx.Item):
	def __init__(self, fileName, index = 0):
		ui.ListBoxEx.Item.__init__(self)
		self.canLoad=0
		self.text=fileName
		self.index = index
		self.textLine=self.__CreateTextLine(fileName)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.text

	def GetIndex(self):
		return self.index

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)

		textLine.SetPosition(4, 0)

		textLine.SetText(fileName)
		textLine.Show()
		return textLine

	def OnSelectedRender(self):
		pass
		
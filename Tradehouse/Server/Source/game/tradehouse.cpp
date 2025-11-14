#include "stdafx.h"
#include "utils.h"
#include "config.h"
#include "char.h"
#include "db.h"
#include <vector>
#include "item.h"
#include "item_manager.h"
#include "desc.h"
#include "tradehouse.h"
#include <sstream>

const char* CreateGetLogQuery(DWORD owner, int offset)
{
	std::stringstream ss;
	//ss << "SELECT * FROM tradehouse.log WHERE id=" << owner << " ORDER BY when_time DESC ";
	//ss << " LIMIT " << offset << ", " << (offset + TRADEHOUSE_ITEM_PACK);

	ss << "SELECT * FROM tradehouse.log WHERE who=" << owner << " ORDER BY when_time DESC ";
	ss << "LIMIT 50";

	return ss.str().c_str();
}

const char* CreateLogQuery(TItem item)
{
	std::stringstream ss;
	ss << "INSERT INTO tradehouse.log VALUES (NULL, ";
	ss << item.owner << ", " << item.vnum << ", " << item.price << ", " << item.count << ", NOW())";

	return ss.str().c_str();
}

const char* CreateAddMoneyToOwner(TItem item)
{
	std::stringstream ss;

	ss << "UPDATE account.account INNER JOIN player.player ON account.id = player.account_id SET ";
	ss << "tradehouse_balance = tradehouse_balance + " << item.price << " ";
	ss << "WHERE player.id = " << item.owner;

	return ss.str().c_str();
}

const char* GetAddItemQuery(TItem item)
{
	std::stringstream ss;
	ss << "INSERT INTO tradehouse.items ";
	ss << "VALUES (NULL, ";
	ss << item.owner << ", " << item.vnum << ", " << item.count << ", ";
	ss << item.price << ", " << (int)item.type << ", " << (int)item.subtype << ", '" << item.owner_name << "', " << item.expire << ", ";

	for (size_t i = 0; i < 7; i++)
	{
		ss << (int)item.bonuses[i].bType << ", ";
	}
	for (size_t i = 0; i < 7; i++)
	{
		ss << (int)item.bonuses[i].sValue << ", ";
	}

	ss << (long)item.sockets[0] << ", ";
	ss << (long)item.sockets[1] << ", ";
	ss << (long)item.sockets[2];
	ss << ")";

	return ss.str().c_str();
}

const char* GetRemoveItemQuery(TItem item)
{
	std::stringstream ss;
	ss << "DELETE FROM tradehouse.items WHERE id=" << item.id;
	ss << " AND owner_id=" << item.owner;

	return ss.str().c_str();
}

const char* GetBuyItemQuery(DWORD unique)
{
	std::stringstream ss;
	ss << "SELECT * FROM tradehouse.items WHERE id=" << unique;

	return ss.str().c_str();
}

void TradeHouse::Init()
{
	vec_Items.clear();
}

void TradeHouse::SendClient(LPCHARACTER ch, std::vector<TItem> items)
{
	if (!ch)
		return;
	
	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseBalance %d", GetPlayerCoin(ch->GetDesc()->GetAccountTable().id));

	TPacketTradehouseItem p;
	p.header = HEADER_GC_TRADEHOUSE_ITEM;

	for (int i = 0; i < items.size(); i++)
	{
		if (i >= TRADEHOUSE_ITEM_PACK)
			continue;

		p.items[i].unique = items[i].id;
		p.items[i].vnum = items[i].vnum;
		p.items[i].price = items[i].price;
		p.items[i].count = (WORD)items[i].count;

		sprintf(p.items[i].owner, items[i].owner_name.c_str());

		p.items[i].expire = items[i].expire;

		for (int j = 0; j < 3; j++)
			p.items[i].alSockets[j] = items[i].sockets[j];

		for (int k = 0; k < 7; k++)
		{
			p.items[i].aAttr[k].bType = items[i].bonuses[k].bType;
			p.items[i].aAttr[k].sValue = items[i].bonuses[k].sValue;
		}

		//ch->ChatPacket(0, "Unique %d S0 %d S1 %d S2 %d", p.items[i].unique, p.items[i].alSockets[0], p.items[i].alSockets[1], p.items[i].alSockets[2]);
	}

	ch->GetDesc()->Packet(&p, sizeof(TPacketTradehouseItem));

	//for (auto & item : items)
	//{
	//	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseItem %d %d %d %d", item.id, item.vnum, item.count, item.price);
	//}
}

void TradeHouse::AddItem(LPCHARACTER ch, int slot, DWORD price)
{
	if (!ch)
		return;

	if (price <= 0)
		return;

	LPITEM item = ch->GetInventoryItem((WORD)slot);

	if (!item)
		return;

	if (true == item->isLocked())
		return;

	if (ch->IsDead())
		return;

	if (ch->GetExchange())
		return;

	if (item->IsExchanging())
		return;

	if (item->IsEquipped())
		return;

	if (IS_SET(item->GetAntiFlag(), ITEM_ANTIFLAG_MYSHOP))
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cannot sell this item."));
		return;
	}

	TItem houseItem;
	//houseItem.owner = ch->GetDesc()->GetAccountTable().id;
	houseItem.owner = ch->GetPlayerID();
	houseItem.vnum = item->GetVnum();
	houseItem.count = item->GetCount();
	houseItem.price = price;
	houseItem.type = item->GetType();
	houseItem.subtype = item->GetSubType();

	for (size_t i = 0; i < 3; i++)
	{
		houseItem.sockets[i] = item->GetSocket(i);
	}

	for (size_t i = 0; i < 7; i++)
	{
		houseItem.bonuses[i].bType = item->GetAttributeType(i);
		houseItem.bonuses[i].sValue = item->GetAttributeValue(i);
	}

	houseItem.owner_name = ch->GetName();
	houseItem.expire = (10 * 24 * 60 * 60) + get_global_time(); // 10 nap

	DBManager::instance().DirectQuery(GetAddItemQuery(houseItem));

	item->SetCount(0);
}

void TradeHouse::GetItem(LPCHARACTER ch, DWORD unique)
{
	if (!ch)
		return;

	std::stringstream ss;
	ss << "SELECT * FROM tradehouse.items WHERE id = " << unique;
	//ss << " AND owner_id=" << ch->GetDesc()->GetAccountTable().id;
	ss << " AND owner_id=" << ch->GetPlayerID();

	int MaxItemCount = 0;
	auto item_vec = GetItemQuery(ss.str().c_str(), MaxItemCount);

	if (item_vec.size() > 1)
	{
		sys_err("PROBLEM! DUPLICATED UNIQUE IN TRADEHOUSE! %d %d", ch->GetDesc()->GetAccountTable().id, unique);
		return;
	}

	if (item_vec.size() < 1)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This item does not exist."));
		return;
	}

	LPITEM item = ITEM_MANAGER::instance().CreateItem(item_vec[0].vnum, item_vec[0].count);
	if (item)
	{
		int pos;
		if ((pos = ch->GetEmptyInventory(item->GetSize())) == -1)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You don't have enough space in your inventory."));
			return;
		}

		DBManager::instance().DirectQuery(GetRemoveItemQuery(item_vec[0]));

		item->ClearAttribute();

		for (size_t i = 0; i < 3; i++) item->SetSocket(i, item_vec[0].sockets[i]);
		for (size_t i = 0; i < 7; i++) item->SetForceAttribute(i, item_vec[0].bonuses[i].bType, item_vec[0].bonuses[i].sValue);

		item->SetAttributes(item_vec[0].bonuses);

		item->AddToCharacter(ch, TItemPos(INVENTORY, pos));
		ITEM_MANAGER::instance().FlushDelayedSave(item);

	}

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseRefresh");

}

int TradeHouse::GetPlayerCoin(DWORD aid)
{
	std::unique_ptr<SQLMsg> msg(DBManager::instance().DirectQuery("SELECT tradehouse_balance FROM account.account WHERE id = %d", aid));
	SQLResult* pRes = msg->Get();

	if (pRes->uiNumRows)
	{
		MYSQL_ROW row;
		while ((row = mysql_fetch_row(pRes->pSQLResult)))
		{
			return atoi(row[0]);
		}
	}

	return 0;
}

bool TradeHouse::ChangePlayerCoin(LPCHARACTER ch, DWORD aid, int value)
{
	if (!ch)
	{
		return false;
	}

	int PCoin = GetPlayerCoin(aid);

	if (value < 0 && PCoin < ::abs(value))
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You don't have enough balance."));
		return false;
	}

	DBManager::instance().DirectQuery("UPDATE account.account SET tradehouse_balance=tradehouse_balance+%i WHERE id=%d", value, aid);

	return true;
}


void TradeHouse::Add_Balance(LPCHARACTER ch, DWORD count)
{
	if (!ch)
		return;

	if (ch->CountSpecifyItem(TRADEHOUSE_BALANCE_VNUM) < (int)count)
		return;

	if (!ChangePlayerCoin(ch, ch->GetDesc()->GetAccountTable().id, (int)count))
		return;

	ch->RemoveSpecifyItem(TRADEHOUSE_BALANCE_VNUM, (int)count);

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseBalance %d", GetPlayerCoin(ch->GetDesc()->GetAccountTable().id));
}

void TradeHouse::Get_Balance(LPCHARACTER ch, DWORD count)
{
	if (!ch)
		return;

	if (count > ITEM_MAX_COUNT)
		return;

	if (!ChangePlayerCoin(ch, ch->GetDesc()->GetAccountTable().id, -(int)count))
		return;

	ch->AutoGiveItem(TRADEHOUSE_BALANCE_VNUM, count);

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseBalance %d", GetPlayerCoin(ch->GetDesc()->GetAccountTable().id));
}

void TradeHouse::BuyItem(LPCHARACTER ch, DWORD unique)
{
	int MaxItemCount = 0;
	auto item_vec = GetItemQuery(GetBuyItemQuery(unique), MaxItemCount);

	if (item_vec.size() > 1)
	{
		sys_err("PROBLEM! DUPLICATED UNIQUE IN TRADEHOUSE! %d %d", ch->GetDesc()->GetAccountTable().id, unique);
		return;
	}

	if (item_vec.size() < 1)
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("This item does not exist."));
		return;
	}

	int pos;
	if ((pos = ch->GetEmptyInventory(3)) == -1)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You don't have enough space in your inventory."));
		return;
	}


	if (!ChangePlayerCoin(ch, ch->GetDesc()->GetAccountTable().id, (-(int)item_vec[0].price)))
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You don't have enough balance."));
		return;
	}

	DBManager::instance().DirectQuery(CreateAddMoneyToOwner(item_vec[0]));

	//DBManager::instance().DirectQuery("UPDATE account.account SET tradehouse_balance=tradehouse_balance+%i WHERE id=%d", item_vec[0].price, item_vec[0].owner);
	DBManager::instance().DirectQuery(GetRemoveItemQuery(item_vec[0]));
	
	LPITEM item = ITEM_MANAGER::instance().CreateItem(item_vec[0].vnum, item_vec[0].count);

	if (!item)
	{
		sys_err("PROBLEM! LOST ITEM IN TRADEHOUSE! %d %d %d", ch->GetDesc()->GetAccountTable().id, item_vec[0].vnum, item_vec[0].count);
		return;
	}

	item->ClearAttribute();
	for (size_t i = 0; i < 3; i++) item->SetSocket(i, item_vec[0].sockets[i]);
	for (size_t i = 0; i < 7; i++) item->SetForceAttribute(i, item_vec[0].bonuses[i].bType, item_vec[0].bonuses[i].sValue);

	item->AddToCharacter(ch, TItemPos(INVENTORY, pos));
	ITEM_MANAGER::instance().FlushDelayedSave(item);

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseRefresh");

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseBalance %d", GetPlayerCoin(ch->GetDesc()->GetAccountTable().id));

	DBManager::instance().DirectQuery(CreateLogQuery(item_vec[0]));

}

void TradeHouse::Show_Items(LPCHARACTER ch, int category, int subcategory, int offset, bool onlyMine, bool onlyExpired, bool asc, int vnum)
{
	if (!ch)
		return;

	std::stringstream ss;
	ss << "SELECT * FROM tradehouse.items ";

	if (onlyMine)
	{
		//ss << "WHERE owner_id=" << ch->GetDesc()->GetAccountTable().id;
		ss << "WHERE owner_id=" << ch->GetPlayerID();
	}
	else
	{
		if (vnum != 0) // Search
		{
			ss << "WHERE vnum=" << vnum << " AND expire > " << get_global_time()+10;
		}
		else // No search, search by categories
		{
			if (subcategory == 254)
				ss << "WHERE category=" << (int)category << " AND expire > " << get_global_time() + 10;
			else
				ss << "WHERE category=" << (int)category << " AND subcategory=" << (int)subcategory << " AND expire > " << get_global_time() + 10;;
		}
	}
	
	if (asc)
		ss << " ORDER BY price ASC,count DESC,id ASC";
	else
		ss << " ORDER BY price DESC,count ASC,id ASC";

	//expired check

	ss << " LIMIT " << offset << ", " << (offset + TRADEHOUSE_ITEM_PACK);

	int MaxItemCount = 0;

	auto items = GetItemQuery(ss.str().c_str(), MaxItemCount);

	ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseInfo %d %d", MaxItemCount, onlyMine);

	SendClient(ch, items);

}

void TradeHouse::SendHistory(LPCHARACTER ch, int offset)
{
	std::unique_ptr<SQLMsg> msg(DBManager::instance().DirectQuery(CreateGetLogQuery(ch->GetPlayerID(), offset)));
	SQLResult* pRes = msg->Get();

	if (pRes->uiNumRows)
	{
		MYSQL_ROW row;
		while ((row = mysql_fetch_row(pRes->pSQLResult)))
		{
			ch->ChatPacket(CHAT_TYPE_COMMAND, "TradehouseHistory %s %s %s %s %s", row[1], row[2], row[3], row[4], row[5]);
		}
	}
}

std::vector<TItem> TradeHouse::GetItemQuery(const char* query, int& num_rows)
{
	std::vector<TItem> items;

	std::unique_ptr<SQLMsg> msg(DBManager::instance().DirectQuery(query));
	SQLResult* pRes = msg->Get();

	num_rows = pRes->uiNumRows;

	if (pRes->uiNumRows)
	{
		TItem item;

		MYSQL_ROW row;
		while ((row = mysql_fetch_row(pRes->pSQLResult)))
		{
			item.id = atoi(row[0]);
			item.owner = atoi(row[1]);
			item.vnum = atoi(row[2]);
			item.count = atoi(row[3]);
			item.price = atoi(row[4]);
			item.type = atoi(row[5]);
			item.subtype = atoi(row[6]);

			item.owner_name = row[7];
			item.expire = atol(row[8]);

			int startPosBonus = 9; // Index of first Bonus Type column
			int startPosValue = 16; // Index of first Bonus Value column
			int startPosSocket = 23; //Index of first Socket column

			for (size_t i = 0; i < 7; i++)
			{
				item.bonuses[i].bType = (BYTE)atoi(row[startPosBonus]);
				item.bonuses[i].sValue = (short)atoi(row[startPosValue]);
				startPosBonus++;
				startPosValue++;
			}

			for (size_t i = 0; i < 3; i++)
			{
				item.sockets[i] = atol(row[startPosSocket]);
				startPosSocket++;
			}

			items.push_back(item);
		}
	}

	return items;
}

#pragma once

#pragma pack(1)
typedef struct STradehouseItem
{
	DWORD id;
	DWORD owner;

	DWORD vnum;
	DWORD count;
	DWORD price;

	std::string owner_name;

	BYTE type;
	BYTE subtype;

	long sockets[3];
	TPlayerItemAttribute bonuses[7];

	long expire;
} TItem; // for serverside statements
#pragma pack()

class TradeHouse : public singleton<TradeHouse>
{
public:

	enum ETradeHouse
	{
		QUERY_REQUEST_ITEM,
		QUERY_GET_BALANCE,
		QUERY_SET_BALANCE,
		QUERY_GET_ITEM,
		QUERY_ADD_ITEM,
		QUERY_BUY_ITEM,
	};

	//TradeHouse();
	//~TradeHouse();

	void Init();

	void SendClient(LPCHARACTER ch, std::vector<TItem> items);

	void AddItem(LPCHARACTER ch, int slot, DWORD price);
	void GetItem(LPCHARACTER ch, DWORD unique);

	int GetPlayerCoin(DWORD aid);
	bool ChangePlayerCoin(LPCHARACTER ch, DWORD aid, int value);

	void Add_Balance(LPCHARACTER ch, DWORD count);

	void Get_Balance(LPCHARACTER ch, DWORD count);

	void BuyItem(LPCHARACTER ch, DWORD unique);

	//int GetCategoryCount(int category, int subcategory);
	void Show_Items(LPCHARACTER ch, int category, int subcategory, int offset, bool onlyMine = false, bool onlyExpired = false, bool asc = true, int vnum = 0);
	void SendHistory(LPCHARACTER ch, int offset);
	std::vector<TItem> GetItemQuery(const char* query, int& num_rows);

protected:
	std::vector<TItem> vec_Items;
};


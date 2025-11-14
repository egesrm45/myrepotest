#pragma once
#include "TradehouseHelper.h"

typedef struct s_game_name_data
{
	std::string name = "";
	DWORD vnum = 0;
} game_name_data;


class PythonTradehouse : public CSingleton<PythonTradehouse>
{
	public:
		PythonTradehouse(void);
		virtual ~PythonTradehouse(void);

		void Clear();
		void UpdateResult(int num, int ownerflag);
		void AppendHistory(const char* v1, const char* v2, const char* v3, const char* v4, const char* v5);
		void Refresh();
		void UpdateBalance(int num);
		void AddItem(TradehouseItem item);
		void ClearItems();
		void AddItemName(std::string name, DWORD vnum);
		std::vector<DWORD> SearchItem(std::string name);

		TradehouseItem GetItemByUnique(DWORD unique);

		std::vector<TradehouseItem> GetCollection() { return Collection; };

		void SetHandler(PyObject* poHandler);

	protected:
		std::vector<TradehouseItem> Collection;
		std::vector<game_name_data> ITEM_NAME_DATA;
		//std::map<const char *, DWORD> ITEM_NAME_MAP;

	private:
		PyObject* m_poTradeHouseHandler;

};


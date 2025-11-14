#include "stdafx.h"
#include "Packet.h"
#include "TradehouseHelper.h"
#include "PythonTradehouse.h"

#include "PythonNetworkStream.h"

PythonTradehouse::PythonTradehouse(void)
{
	m_poTradeHouseHandler = NULL;
	Clear();
}

PythonTradehouse::~PythonTradehouse(void)
{
}

void PythonTradehouse::SetHandler(PyObject* poHandler)
{
	m_poTradeHouseHandler = poHandler;
}

void PythonTradehouse::Clear()
{
	Collection.clear();
	ITEM_NAME_DATA.clear();
}

void PythonTradehouse::UpdateResult(int num, int ownerflag)
{
	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "UpdateResultBoard", Py_BuildValue("(ii)", num, ownerflag));
	}
}

void PythonTradehouse::AppendHistory(const char * v1, const char* v2, const char* v3, const char* v4, const char* v5)
{
	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "AppendHistory", Py_BuildValue("(sssss)", v1, v2, v3, v4, v5));
	}
}

void PythonTradehouse::Refresh()
{
	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "Refresh", Py_BuildValue("()"));
	}
}

void PythonTradehouse::UpdateBalance(int num)
{
	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "UpdateBalance", Py_BuildValue("(i)", num));
	}
}

void PythonTradehouse::AddItem(TradehouseItem item)
{
	if (item.vnum == 0)
		return;

	Collection.push_back(item);

	//TraceError("Add item %d %d %d", item.vnum, item.aAttr[0].bType, item.aAttr[0].sValue);

	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "AddItemData", Py_BuildValue("(iiiiis)", item.unique, item.vnum, item.count, item.price, item.expire, item.owner));
	}
}

void PythonTradehouse::ClearItems()
{
	Collection.clear();

	if (m_poTradeHouseHandler)
	{
		PyCallClassMemberFunc(m_poTradeHouseHandler, "ClearItems", Py_BuildValue("()"));
	}
}

void PythonTradehouse::AddItemName(std::string name, DWORD vnum)
{
	game_name_data d;
	d.name = name;
	d.vnum = vnum;

	ITEM_NAME_DATA.push_back(d);
}

std::vector<DWORD> PythonTradehouse::SearchItem(std::string name)
{
	std::vector<DWORD> items;
	items.clear();

	for (auto & element : ITEM_NAME_DATA)
	{
		if (element.name.find(name) != string::npos)
		{
			items.push_back(element.vnum);
		}
	}

	//if (m_poTradeHouseHandler)
	//	PyCallClassMemberFunc(m_poTradeHouseHandler, "TestFunc", Py_BuildValue("(i)", 10));

	return items;
}

TradehouseItem PythonTradehouse::GetItemByUnique(DWORD unique)
{
	for (auto& element : Collection)
		if (element.unique == unique)
			return element;

	return TradehouseItem();
}

PyObject* itemSearch(PyObject* poSelf, PyObject* poArgs)
{
	char* name;
	if (!PyTuple_GetString(poArgs, 0, &name))
		return Py_BuildException();

	auto vnums = PythonTradehouse::Instance().SearchItem(name);

	PyObject* python_val = PyList_New(vnums.size());
	for (int i = 0; i < vnums.size(); ++i)
	{
		PyObject* python_int = Py_BuildValue("i", vnums[i]);
		PyList_SetItem(python_val, i, python_int);
	}

	return python_val;

	//return Py_BuildValue("{items}", );
}


PyObject* itemSetHandler(PyObject* poSelf, PyObject* poArgs)
{
	PyObject* poEventHandler;
	if (!PyTuple_GetObject(poArgs, 0, &poEventHandler))
		return Py_BuildException();

	PythonTradehouse::Instance().SetHandler(poEventHandler);
	return Py_BuildNone();
}

PyObject* itemGetCount(PyObject* poSelf, PyObject* poArgs)
{
	int iValue = PythonTradehouse::Instance().GetCollection().size();
	return Py_BuildValue("i", iValue);
}

PyObject* itemGetInfo(PyObject* poSelf, PyObject* poArgs)
{
	int unique;
	if (!PyTuple_GetInteger(poArgs, 0, &unique))
		return Py_BuildException();

	int idx;
	if (!PyTuple_GetInteger(poArgs, 1, &idx))
		return Py_BuildException();

	TradehouseItem item = PythonTradehouse::Instance().GetItemByUnique(unique);

	if (idx == 0)
	{
		PyObject* bonus_list = PyList_New(7);

		for (int i = 0; i < 7; ++i)
		{
			PyObject* bonus_attr = PyList_New(2);

			PyList_SetItem(bonus_attr,0, Py_BuildValue("i", (int)item.aAttr[i].bType));
			PyList_SetItem(bonus_attr,1, Py_BuildValue("i", (int)item.aAttr[i].sValue));


			PyList_SetItem(bonus_list, i, bonus_attr);
		}

		return bonus_list;
	}
	else if (idx == 1)
	{

		PyObject* socket_list = PyList_New(3);
		for (int i = 0; i < 3; ++i)
		{
			PyObject* python_int = Py_BuildValue("i", item.alSockets[i]);
			PyList_SetItem(socket_list, i, python_int);
		}

		return socket_list;
	}

	return Py_BuildValue("i", item.vnum);
}

void inittradehouse()
{
	static PyMethodDef s_methods[] =
	{
		{ "SearchItem",						itemSearch,						METH_VARARGS },
		{ "GetCount",						itemGetCount,						METH_VARARGS },

		{ "GetInfo",						itemGetInfo,						METH_VARARGS },

		{ "SetHandler",						itemSetHandler,						METH_VARARGS },

		{ NULL,							NULL,							NULL },
	};
	PyObject* poModule = Py_InitModule("tradehouse", s_methods);


}
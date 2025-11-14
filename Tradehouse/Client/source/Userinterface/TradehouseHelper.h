#pragma once

#pragma pack(push)
#pragma pack(1)
typedef struct TPlayerItemAttributeTradeHouse
{
	unsigned char        bType;
	short       sValue;
} TPlayerItemAttributeTradeHouse;

typedef struct STItem
{
	unsigned long unique;
	unsigned long vnum;
	unsigned long price;
	unsigned short count;
	char owner[25];
	long alSockets[3];
	TPlayerItemAttributeTradeHouse aAttr[7];
	long expire;
} TradehouseItem;
#pragma pack()

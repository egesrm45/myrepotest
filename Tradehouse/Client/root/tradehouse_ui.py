import uiScriptLocale

WINDOW_HEIGHT = 530
WINDOW_WIDTH = 450

window = {
	"name" : "TradehouseWindow",
	"style" : ("movable", "float",),

	"x" : 400,
	"y" : 200,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : WINDOW_WIDTH -10,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":(WINDOW_WIDTH - 10) / 2, "y":3, "text":"Kereskedõház", "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "result_board",
					"type" : "thinboard",
					"style" : ("attach",),
					
					"x" : WINDOW_WIDTH / 2 - 15,
					"y" : 35,

					"width" : WINDOW_WIDTH - 220,
					"height" : 30,					
					
					"children" : 
					(
						{ "name":"ResultText", "type":"text", "x":10, "y":8, "text":"Találat: 0 darab", "text_horizontal_align":"left" },
					),
					
				},
				
				{
					"name" : "item_board",
					"type" : "thinboard",
					"style" : ("attach",),
					
					"x" : WINDOW_WIDTH / 2 - 15,
					"y" : 80,

					"width" : WINDOW_WIDTH - 220,
					"height" : WINDOW_HEIGHT - 90,					
					
				},

				{
					"name" : "main_board",
					"type" : "thinboard",
					"style" : ("attach",),
					
					"x" : 12,
					"y" : 35,

					"width" : WINDOW_WIDTH - 260,
					"height" : WINDOW_HEIGHT - 45,					
					
				},
				
			),
		},
	),
}

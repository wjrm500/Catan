config = {
    'resource_types': {
        'brick': {
            'color': '#E56C63',
            'count': 3
        },
        'desert': {
            'color': '#F0A055',
            'count': 1
        },
        'grain': {
            'color': '#F0DA6C',
            'count': 4
        },
        'lumber': {
            'color': '#8BC38F',
            'count': 4
        },
        'ore': {
            'color': '#DBDCDD',
            'count': 3
        },
        'wool': {
            'color': '#D7F0B8',
            'count': 4
        }
    },
    'port_types': {
        'brick': {
            'cost': 2,
            'count': 1
        },
        'general': {
            'cost': 3,
            'count': 4
        },
        'grain': {
            'cost': 2,
            'count': 1
        },
        'lumber': {
            'cost': 2,
            'count': 1
        },
        'ore': {
            'cost': 2,
            'count': 1
        },
        'wool': {
            'cost': 2,
            'count': 1
        }
    },
    'roll_num_counts': {
        2: 1,
        3: 2,
        4: 2,
        5: 2,
        6: 2,
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 1
    },
    'development_card_types': {
        'knight': {
            'color': '#9400D3',
            'count': 14
        },
        'monopoly': {
            'color': '#6B8E23',
            'count': 2
        },
        'road_building': {
            'color': '#6B8E23',
            'count': 2
        },
        'victory_point': {
            'color': '#FF8C00',
            'count': 5
        },
        'year_of_plenty': {
            'color': '#6B8E23',
            'count': 2
        }
    },
    'player_colors': {'red': '#FF0000', 'aqua': '#00FFFF', 'lime': '#00FF00', 'yellow': '#FFFF00'},
    'actions': {
        'BUILD_ROAD': {
            'name': 'Build road',
            'cost': {
                'resources': ['1 brick', '1 lumber'],
                'other': ['1 road token', '1 roadworthy line']
            }
        },
        'BUILD_VILLAGE': {
            'name': 'Build village',
            'cost': {
                'resources': ['1 brick', '1 grain', '1 lumber', '1 wool'],
                'other': ['1 village token', '1 settleworthy node']
            }
        },
        'UPGRADE_SETTLEMENT': {
            'name': 'Upgrade village to city',
            'cost': {
                'resources': ['2 grain', '3 ore'],
                'other': ['1 city token', '1 village on board']
            }
        },
        'BUY_DEVELOPMENT_CARD': {
            'name': 'Buy a development card',
            'cost': {
                'resources': ['1 grain', '1 ore', '1 wool'],
                'other': ['1 development card in deck']
            }
        },
        'USE_DEVELOPMENT_CARD': {
            'name': 'Use a development card',
            'cost': {
                'other': ['1 development card in hand']
            }
        },
        'TRADE_WITH_BANK': {
            'name': 'Trade with the bank'
        },
        'SWAP_CARDS': {
            'name': 'Swap two cards with opponent',
            'cost': {
                'other': ['2 resource cards in hand', "2 resource cards in opponent's hand", '$game_token_cost game token'] ### TODO: Variable num. of game tokens
            }
        },
        'MOVE_ROBBER_TO_DESERT': {
            'name': 'Move robber to desert hex',
            'cost': {
                'other': ['$game_token_cost game token'] ### TODO: Variable num. of game tokens
            }
        }
    }
}
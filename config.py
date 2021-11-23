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
    'actions': [
            {
                'name': 'Build road',
                'const': 'BUILD_ROAD',
                'cost': {
                    'resource_cards': {
                        'brick': 1,
                        'lumber': 1
                    },
                    'other_items': {
                        'game_token': 1
                    }
                }
            },
            {
                'name': 'Build settlement',
                'const': 'BUILD_SETTLEMENT',
                'cost': {
                    'resource_cards': {
                        'brick': 1,
                        'grain': 1,
                        'lumber': 1,
                        'wool': 1
                    },
                    'other_items': {
                        'available_node': 1,
                        'settlement_token': 1
                    }
                }
            },
            {
                'name': 'Upgrade settlement to city',
                'const': 'UPGRADE_SETTLEMENT',
                'cost': {
                    'resource_cards': {
                        'grain': 2,
                        'ore': 3
                    },
                    'other_items': {
                        'available_settlement': 1,
                        'city_token': 1
                    }
                }
            },
            {
                'name': 'Buy a development card',
                'const': 'BUY_DEVELOPMENT_CARD',
                'cost': {
                    'resource_cards': {
                        'grain': 1,
                        'ore': 1,
                        'wool': 1
                    },
                    'other_items': {
                        'development_card_in_deck': 1 ### Maybe just have unlimited
                    }
                }
            },
            {
                'name': 'Use a development card',
                'const': 'USE_DEVELOPMENT_CARD',
                'cost': {
                    'other_items': {
                        'development_card_in_hand': 1
                    }
                }
            },
            {
                'name': 'Trade with the bank',
                'const': 'BANK_TRADE',
                'cost': {
                    'other_items': {
                        'resource_card_in_hand': 'variable'
                    }
                }
            },
            {
                'name': 'Swap two cards with opponent',
                'const': 'SWAP_CARDS',
                'cost': {
                    'other_items': {
                        'game_token': 'variable', ### 2 if winning else 1
                        'resource_card_in_hand': 2,
                        'resource_card_in_opponent_hand': 2
                    }
                }
            },
            {
                'name': 'Move robber to desert hex',
                'const': 'MOVE_ROBBER_TO_DESERT',
                'cost': {
                    'other_items': {
                        'game_token': 'variable' ### 2 if winning else 1
                    }
                }
            }
    ]
}
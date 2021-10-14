import numpy as np
import typing
import unittest

from quatrominos import Quatrominos


class TileFactory(object):
    tile0123 = (0, 1, 2, 3)
    tile1111 = (1, 1, 1, 1)
    tile1113 = (1, 1, 1, 3)
    tile1114 = (1, 1, 1, 4)
    tile1145 = (1, 1, 4, 5)
    tile1212 = (1, 2, 1, 2)
    tile1234 = (1, 2, 3, 4)
    tile1313 = (1, 3, 1, 3)
    tile1411 = (1, 4, 1, 1)
    tile1414 = (1, 4, 1, 4)
    tile1425 = (1, 4, 2, 5)
    tile1522 = (1, 5, 2, 2)
    tile2222 = (2, 2, 2, 2)
    tile3333 = (3, 3, 3, 3)
    tile2411 = (2, 4, 1, 1)
    tile2224 = (2, 2, 2, 4)
    tile4121 = (4, 1, 2, 1)
    tile5315 = (5, 3, 1, 5)


class GameStateFactory(object):

    @staticmethod
    def get_board_empty() -> typing.Tuple[Quatrominos, typing.List[typing.Tuple[int, int]], typing.List[bool], int]:
        player0 = {TileFactory.tile0123}
        player1 = {TileFactory.tile0123}
        board = np.full((5, 5, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)

        return game_state, [(2, 2)], [True], 4

    @staticmethod
    def get_board_single_tile() -> typing.Tuple[Quatrominos, typing.List[typing.Tuple[int, int]], typing.List[bool], int]:
        player0 = {TileFactory.tile0123}
        player1 = {TileFactory.tile0123}
        board = np.full((5, 5, 4), -1)
        board[2, 2] = TileFactory.tile1111
        game_state = Quatrominos(player0, player1, board, 0)

        return game_state, [(1, 2), (2, 3), (3, 2), (2, 1)], [False, False, False, True], 4

    @staticmethod
    def get_board_five_tiles() -> typing.Tuple[Quatrominos,
                                               typing.List[typing.Tuple[int, int]],
                                               typing.List[bool], int]:
        player0 = {TileFactory.tile2222}
        player1 = {TileFactory.tile0123}
        board = np.full((5, 5, 4), -1)
        board[0, 2] = TileFactory.tile1313
        board[1, 2] = TileFactory.tile1212
        board[2, 2] = TileFactory.tile1234
        board[2, 3] = TileFactory.tile2222
        board[2, 4] = TileFactory.tile1212
        game_state = Quatrominos(player0, player1, board, 0)

        return game_state, \
            [(0, 1), (0, 3), (1, 1), (1, 3), (1, 4), (2, 1), (3, 2), (3, 3), (3, 4)], \
            [False, False, True, True, False, False, False, True, False], \
            12

    @staticmethod
    def get_small_board_eight_tiles() -> typing.Tuple[Quatrominos,
                                                      typing.List[typing.Tuple[int, int]],
                                                      typing.List[bool], int]:
        player0 = {TileFactory.tile2411}
        player1 = {TileFactory.tile0123}
        board = np.full((3, 3, 4), -1)
        board[0, 0] = TileFactory.tile0123
        board[0, 1] = TileFactory.tile1111
        board[0, 2] = TileFactory.tile1411
        board[1, 1] = TileFactory.tile1234
        board[2, 0] = TileFactory.tile1313
        board[2, 1] = TileFactory.tile3333
        board[2, 2] = TileFactory.tile1313
        game_state = Quatrominos(player0, player1, board, 0)

        return game_state, [(1, 0), (1, 2)], [True, False], 1

    @staticmethod
    def get_small_board_adversarial() -> Quatrominos:
        player0 = {TileFactory.tile1425, TileFactory.tile1522}
        player1 = {TileFactory.tile2222, TileFactory.tile1145}
        board = np.full((3, 3, 4), -1)
        board[0, 0] = TileFactory.tile5315
        board[0, 1] = TileFactory.tile1113
        board[0, 2] = TileFactory.tile4121
        board[1, 1] = TileFactory.tile1234
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state

    @staticmethod
    def get_big_board() -> Quatrominos:
        player0 = {
            TileFactory.tile1111, TileFactory.tile1113,
            TileFactory.tile1212, TileFactory.tile1313
        }
        player1 = {
            TileFactory.tile1414, TileFactory.tile2222,
            TileFactory.tile3333, TileFactory.tile2411,
        }
        board = np.full((5, 5, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state


class TestQuatrominos(unittest.TestCase):

    def test_get_rotated_tile(self):
        self.assertEqual(Quatrominos.get_rotated_tile(TileFactory.tile0123, 0), TileFactory.tile0123)
        self.assertEqual(Quatrominos.get_rotated_tile(TileFactory.tile0123, 1), (3, 0, 1, 2))
        self.assertEqual(Quatrominos.get_rotated_tile(TileFactory.tile0123, 2), (2, 3, 0, 1))
        self.assertEqual(Quatrominos.get_rotated_tile(TileFactory.tile0123, 3), (1, 2, 3, 0))
        self.assertEqual(Quatrominos.get_rotated_tile(TileFactory.tile0123, 4), TileFactory.tile0123)

    def test_adjacent_locations_empty_board(self):
        game_state, locations, _, _ = GameStateFactory.get_board_empty()
        result = game_state.adjacent_locations()
        self.assertEqual(set(locations), result)

    def test_adjacent_locations_single_tile(self):
        game_state, locations, _, _ = GameStateFactory.get_board_single_tile()
        result = game_state.adjacent_locations()
        self.assertEqual(set(locations), result)

    def test_adjacent_locations_five_tiles(self):
        game_state, locations, _, _ = GameStateFactory.get_board_five_tiles()
        result = game_state.adjacent_locations()
        self.assertEqual(set(locations), result)

    def test_adjacent_locations_eight_tiles(self):
        game_state, locations, _, _ = GameStateFactory.get_small_board_eight_tiles()
        result = game_state.adjacent_locations()
        self.assertEqual(set(locations), result)

    def test_can_place_given_tile_empty_board(self):
        game_state, locations, placements, _ = GameStateFactory.get_board_empty()
        for location, placement in zip(locations, placements):
            tile = list(game_state.player_hand[0])[0]
            result = game_state.can_place_given_tile(location[0], location[1], tile)
            self.assertEqual(placement, result)

    def test_can_place_given_one_tile(self):
        game_state, locations, placements, _ = GameStateFactory.get_board_single_tile()
        for location, placement in zip(locations, placements):
            tile = list(game_state.player_hand[0])[0]
            result = game_state.can_place_given_tile(location[0], location[1], tile)
            self.assertEqual(placement, result)

    def test_can_place_given_five_tiles(self):
        game_state, locations, placements, _ = GameStateFactory.get_board_five_tiles()
        for location, placement in zip(locations, placements):
            tile = list(game_state.player_hand[0])[0]
            result = game_state.can_place_given_tile(location[0], location[1], tile)
            self.assertEqual(placement, result)

    def test_can_place_given_small_board(self):
        game_state, locations, placements, _ = GameStateFactory.get_small_board_eight_tiles()
        for location, placement in zip(locations, placements):
            tile = list(game_state.player_hand[0])[0]
            result = game_state.can_place_given_tile(location[0], location[1], tile)
            self.assertEqual(placement, result)

    def test_count_available_moves_empty_board(self):
        game_state, _, _, num_moves = GameStateFactory.get_board_empty()
        result = game_state.count_available_moves(game_state.player_hand[0])
        self.assertEqual(num_moves, result)

    def test_count_available_moves_one_tile(self):
        game_state, _, _, num_moves = GameStateFactory.get_board_single_tile()
        result = game_state.count_available_moves(game_state.player_hand[0])
        self.assertEqual(num_moves, result)

    def test_count_available_moves_five_tiles(self):
        game_state, _, _, num_moves = GameStateFactory.get_board_five_tiles()
        result = game_state.count_available_moves(game_state.player_hand[0])
        self.assertEqual(num_moves, result)

    def test_count_available_moves_small_board(self):
        game_state, _, _, num_moves = GameStateFactory.get_small_board_eight_tiles()
        result = game_state.count_available_moves(game_state.player_hand[0])
        self.assertEqual(num_moves, result)

    def test_check_current_player_lost_midgame(self):
        game_state, _, _, _ = GameStateFactory.get_small_board_eight_tiles()
        result = game_state.check_current_player_lost()
        self.assertFalse(result)

    def test_check_current_player_lost_opponent_notiles(self):
        game_state, _, _, _ = GameStateFactory.get_small_board_eight_tiles()
        game_state.player_hand[1] = {}
        result = game_state.check_current_player_lost()
        self.assertTrue(result)

    def test_check_current_player_lost_nomoves(self):
        game_state, _, _, _ = GameStateFactory.get_small_board_eight_tiles()
        game_state.player_hand[0] = {TileFactory.tile3333}
        result = game_state.check_current_player_lost()
        self.assertTrue(result)

    def test_current_player_can_win_eight_tiles(self):
        game_state, _, _, _ = GameStateFactory.get_small_board_eight_tiles()
        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_current_player_can_win_complex_p0(self):
        game_state = GameStateFactory.get_small_board_adversarial()
        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_current_player_can_win_big(self):
        game_state = GameStateFactory.get_big_board()
        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_current_player_can_win_complex_p1(self):
        game_state = GameStateFactory.get_small_board_adversarial()
        game_state.player_on_turn = 1
        result = game_state.current_player_can_win()
        self.assertFalse(result)

    def test_best_move_greedy(self):
        game_state = GameStateFactory.get_small_board_adversarial()
        result = game_state.best_move_greedy()
        self.assertEqual((1, 2, (2, 1, 5, 2)), result)

        game_state.board[1, 2] = (2, 1, 5, 2)
        game_state.player_on_turn = 1
        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_print(self):

        board = np.full((3, 3, 4), -1)
        board[1, 1] = [1, 1, 1, 1]
        board[1, 2] = [3, 1, 4, 1]
        game = Quatrominos(set(), set(), board, 0)
        game.print_current_state()



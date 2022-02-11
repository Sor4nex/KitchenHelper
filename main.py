# imports
import sys
import sqlite3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


# Window classes
class MainAppWindow(QMainWindow):
    # class of main window of an app
    def __init__(self):
        super().__init__()
        uic.loadUi('helpingElements/uiFolder/ProjectUi3.ui', self)
        self.initUI()

    def initUI(self) -> None:
        # window setups
        self.setWindowTitle('Помощник Повара')

        # other
        self.con = sqlite3.connect(
            'helpingElements/База Данных/ProjectDataBase.sqlite')
        self.cur = self.con.cursor()
        pic = QPixmap('helpingElements/no.jpg')
        pic = pic.scaled(300, 300)
        self.picture_recipe.setPixmap(pic)

        # widget setups
        self.recipe_recipe.setReadOnly(True)

        # recipe list positions setups
        self.get_data_from_base()

        # connections and hooks(btns and func)
        self.add_recipe.clicked.connect(self.add_recipe_func)
        self.list_recipe_available.itemDoubleClicked.connect(self.show_recipe)
        self.recipe_list_refresh.clicked.connect(self.get_data_from_base)
        self.refresh_list_ingredients.clicked.connect(self.get_data_from_base)
        self.remove_recipe.clicked.connect(self.delete_recipe_func)
        self.change_recipe.clicked.connect(self.change_recipe_func)
        self.add_new_ingredient.clicked.connect(self.add_ing_func)
        self.ingredients_ingredients.itemDoubleClicked.connect(
            self.show_ingred)
        self.delete_ingredient.clicked.connect(self.delete_ingred_func)
        self.save_ingredient_change.clicked.connect(self.save_ingred_func)
        self.sort_name_up.clicked.connect(self.alf_sort_recipe)
        self.sort_name_down.clicked.connect(self.alf_sort_recipe_reversed)
        self.sort_ingredients.clicked.connect(self.ingred_sort_recipe)

    def get_data_from_base(self) -> None:
        # method, that get all current data about recipes from DB
        self.recipes_classes = list()
        self.ingredients_classes = list()
        self.ingredients_numbers = list()
        recipes_from_base = self.cur.execute(
            """SELECT * FROM recipes""").fetchall()
        ingredients_from_base = self.cur.execute(
            '''SELECT * FROM ingredients''').fetchall()
        self.last_used = None
        self.list_recipe_available.clear()
        self.ingredients_ingredients.clear()
        self.ingredient_name.clear()
        self.ingredient_count.setValue(0)
        for el in ingredients_from_base:
            iter_ingr_var = Ingredient(el[0], el[1], el[2])
            self.ingredients_classes.append(iter_ingr_var)
            self.ingredients_numbers.append(el[0])
            self.ingredients_ingredients.addItem(
                str(el[0]) + ': ' + str(el[1]) + '\t\t колличество: ' + str(
                    el[2]))
        for elem in recipes_from_base:
            iter_recipe_var = Recipe(elem[0], elem[1], elem[2], elem[3], None)
            self.recipes_classes.append(iter_recipe_var)
            inp_value = (str(self.recipes_classes.index(
                iter_recipe_var) + 1) + ': ' + str(iter_recipe_var))
            if (elem[1] != ''):
                inp_value = QListWidgetItem(inp_value)
                inp_value.setForeground(
                    self.check_count_of_ingred_in_recipe(elem[1]))
            self.list_recipe_available.addItem(inp_value)
        self.set_default_recipe()

    def alf_sort_recipe(self) -> None:
        # method, that sorts recipes list in alphabet order
        self.recipes_classes = list()
        self.ingredients_classes = list()
        self.ingredients_numbers = list()
        recipes_from_base = self.cur.execute(
            '''SELECT * FROM recipes ORDER BY recipeName''').fetchall()
        ingredients_from_base = self.cur.execute(
            '''SELECT * FROM ingredients''').fetchall()
        self.last_used = None
        self.list_recipe_available.clear()
        self.ingredients_ingredients.clear()
        self.ingredient_name.clear()
        self.ingredient_count.setValue(0)
        for el in ingredients_from_base:
            iter_ingr_var = Ingredient(el[0], el[1], el[2])
            self.ingredients_classes.append(iter_ingr_var)
            self.ingredients_numbers.append(el[0])
            self.ingredients_ingredients.addItem(
                str(el[0]) + ': ' + str(el[1]) + '\t\t колличество: ' + str(
                    el[2]))
        for elem in recipes_from_base:
            iter_recipe_var = Recipe(elem[0], elem[1], elem[2], elem[3], None)
            self.recipes_classes.append(iter_recipe_var)
            inp_value = (str(self.recipes_classes.index(
                iter_recipe_var) + 1) + ': ' + str(iter_recipe_var))
            if (elem[1] != ''):
                inp_value = QListWidgetItem(inp_value)
                inp_value.setForeground(
                    self.check_count_of_ingred_in_recipe(elem[1]))
            self.list_recipe_available.addItem(inp_value)
        self.set_default_recipe()

    def alf_sort_recipe_reversed(self) -> None:
        # method, that sorts recipes list in reversed alphabet order
        self.recipes_classes = list()
        self.ingredients_classes = list()
        self.ingredients_numbers = list()
        recipes_from_base = self.cur.execute(
            """SELECT * FROM recipes ORDER BY recipeName""").fetchall()[::-1]
        ingredients_from_base = self.cur.execute(
            '''SELECT * FROM ingredients''').fetchall()
        self.last_used = None
        self.list_recipe_available.clear()
        self.ingredients_ingredients.clear()
        self.ingredient_name.clear()
        self.ingredient_count.setValue(0)
        for el in ingredients_from_base:
            iter_ingr_var = Ingredient(el[0], el[1], el[2])
            self.ingredients_classes.append(iter_ingr_var)
            self.ingredients_numbers.append(el[0])
            self.ingredients_ingredients.addItem(
                str(el[0]) + ': ' + str(el[1]) + '\t\t колличество: ' + str(
                    el[2]))
        for elem in recipes_from_base:
            iter_recipe_var = Recipe(elem[0], elem[1], elem[2], elem[3], None)
            self.recipes_classes.append(iter_recipe_var)
            inp_value = (str(self.recipes_classes.index(
                iter_recipe_var) + 1) + ': ' + str(iter_recipe_var))
            if (elem[1] != ''):
                inp_value = QListWidgetItem(inp_value)
                inp_value.setForeground(
                    self.check_count_of_ingred_in_recipe(elem[1]))
            self.list_recipe_available.addItem(inp_value)
        self.set_default_recipe()

    def ingred_sort_recipe(self) -> None:
        # method, that sorts recipes depending on availability of ingredients
        self.recipes_classes = list()
        self.ingredients_classes = list()
        self.ingredients_numbers = list()
        recipes_from_base = self.cur.execute(
            """SELECT * FROM recipes""").fetchall()
        ingredients_from_base = self.cur.execute(
            '''SELECT * FROM ingredients''').fetchall()
        self.last_used = None
        self.list_recipe_available.clear()
        self.ingredients_ingredients.clear()
        self.ingredient_name.clear()
        self.ingredient_count.setValue(0)
        for el in ingredients_from_base:
            iter_ingr_var = Ingredient(el[0], el[1], el[2])
            self.ingredients_classes.append(iter_ingr_var)
            self.ingredients_numbers.append(el[0])
            self.ingredients_ingredients.addItem(
                str(el[0]) + ': ' + str(el[1]) + '\t\t колличество: ' + str(
                    el[2]))
        for elem in recipes_from_base:
            iter_recipe_var = Recipe(elem[0], elem[1], elem[2], elem[3],
                                     self.check_count_of_ingred_in_recipe_bool(
                                         elem[1]))
            self.recipes_classes.append(iter_recipe_var)
        self.recipes_classes.sort(
            key=lambda x: True if (x.get_all_ingreds() is True) else False,
            reverse=True)
        for iter_recipe_var in self.recipes_classes:
            inp_value = (str(self.recipes_classes.index(
                iter_recipe_var) + 1) + ': ' + str(iter_recipe_var))
            inp_value = QListWidgetItem(inp_value)
            inp_value.setForeground(self.check_count_of_ingred_in_recipe(
                iter_recipe_var.get_recipe_ingred()))
            self.list_recipe_available.addItem(inp_value)
        self.set_default_recipe()

    def add_ing_func(self) -> None:
        # method, that adds new ingredient
        data = AddIngredientWindow()
        if (data.exec_()):
            values = data.accepted()
            self.cur.execute('''INSERT INTO ingredients(ingredientsId,
            IngredientName, ingredients_count) VALUES
            (?, ?, ?)''', (values[1], values[0], values[2]))
            self.con.commit()
            self.get_data_from_base()
        else:
            pass

    def change_recipe_func(self) -> None:
        # method, that changes smth in selected recipe
        try:
            give_in_func = (
                self.recipes_classes[int(
                    self.list_recipe_available.currentItem().text().split(':')[
                        0]) - 1])()
            data = ChangeRecipeWindow(give_in_func[0], give_in_func[1],
                                      give_in_func[2], give_in_func[3])
            if (data.exec_()):
                values = data.accepted()
                # gets name, ingredients, recipe, photo
                self.cur.execute('''UPDATE recipes
                        SET usedIngredientsID = ?, description = ?,
                        pictureName = ? WHERE recipeName = ?''',
                                 (values[1], values[2], values[3], values[0]))
                self.con.commit()
                self.get_data_from_base()
            else:
                pass
        except AttributeError:
            pass

    def add_recipe_func(self) -> None:
        # method, that adds recipes into DB
        data = AddRecipeWindow()
        if (data.exec_()):
            values = data.accepted()
            # gets name, ingredients, recipe, photo
            if (values[0] == ''):
                values[0] = 'Неизвестный рецепт'
            self.cur.execute("""INSERT INTO recipes(recipeName,
            usedIngredientsID, description, pictureName) VALUES
            (?, ?, ?, ?)""", (
                values[0], values[1], values[2], values[3]))
            self.con.commit()
            self.get_data_from_base()
        else:
            pass

    def delete_recipe_func(self) -> None:
        # method, that deletes recipes out of DB
        try:
            recipe_name = self.recipes_classes[int(
                self.list_recipe_available.currentItem().text().split(':')[
                    0]) - 1]
            data = CheckAssuranceWindow()
            if (data.exec_()):
                self.cur.execute(
                    '''DELETE FROM recipes WHERE recipeName = ?''',
                    (str(recipe_name),))
                self.con.commit()
                self.get_data_from_base()
            else:
                pass
        except AttributeError:
            pass

    def set_items(self, lst) -> None:
        # method, that open recipe in left window
        self.list_ingredients_available_4.clear()
        self.recipe_recipe.clear()
        self.picture_recipe.clear()
        pic = QPixmap('Photo/' + str(lst[3]))
        if (pic.isNull()):
            pic = QPixmap('helpingElements/no.jpg')
            pic = pic.scaled(300, 300)
            self.picture_recipe.setPixmap(pic)
        else:
            pic = pic.scaled(300, 300)
            self.picture_recipe.setPixmap(pic)
        for elem in str(lst[1]).split():
            try:
                ind_el_taken = self.ingredients_numbers.index(int(elem))
                values = self.ingredients_classes[ind_el_taken]()
                inp_value = (str(elem) + ': ' + str(values[1]))
                inp_value_item = QListWidgetItem(inp_value)
                inp_value_item.setForeground(self.check_count_of_ingred(elem))
                self.list_ingredients_available_4.addItem(inp_value_item)
            except ValueError:
                self.list_ingredients_available_4.addItem(
                    str(elem) + ': ' + 'Неизвестный ингредиент')
        self.recipe_recipe.setPlainText(lst[2])

    def show_recipe(self) -> None:
        # method, that helps set_item() method to open recipe.
        recipe_ind = int(self.sender().currentItem().text().split(':')[0]) - 1
        self.set_items(self.recipes_classes[recipe_ind]())

    def set_default_recipe(self) -> None:
        # method, that cleans the right show up recipe window
        self.picture_recipe.clear()
        self.recipe_recipe.clear()
        self.list_ingredients_available_4.clear()
        pic = QPixmap('helpingElements/no.jpg')
        pic = pic.scaled(300, 300)
        self.picture_recipe.setPixmap(pic)

    def show_ingred(self) -> None:
        # method, that show the name and count of selected ingredient
        ind_el_taken = int(self.sender().currentItem().text().split(':')[0])
        ind_el_taken2 = int(self.ingredients_numbers.index(ind_el_taken))
        self.last_used = str(ind_el_taken)
        values_taken = self.ingredients_classes[ind_el_taken2]()
        self.ingredient_name.setText(str(values_taken[1]))
        self.ingredient_count.setValue(values_taken[2])

    def delete_ingred_func(self) -> None:
        # method, that deletes the ingredient
        try:
            ingred_numm = \
                self.ingredients_ingredients.currentItem().text().split(':')[0]
            data = CheckAssuranceWindow()
            if (data.exec_()):
                self.cur.execute(
                    '''DELETE FROM ingredients WHERE ingredientsId = ?''',
                    (str(ingred_numm),))
                self.con.commit()
                self.get_data_from_base()
            else:
                pass
        except AttributeError:
            pass

    def save_ingred_func(self) -> None:
        # method, that save the ingredients changes(count, name)
        if (self.last_used is not None):
            self.cur.execute(
                '''UPDATE ingredients SET ingredientName = ?,
                ingredients_count = ? WHERE ingredientsId = ?''',
                (str(self.ingredient_name.text()),
                 str(self.ingredient_count.value()), self.last_used))
            self.con.commit()
            self.get_data_from_base()
        else:
            pass

    def check_count_of_ingred(self, ind_ingr: str) -> QColor:
        # method, that returns color, if user have ingredient, thats id given
        try:
            ind_taken_el = self.ingredients_numbers.index(int(ind_ingr))
            if (int(self.ingredients_classes[ind_taken_el].get_count()) > 0):
                return QColor(0, 158, 31)
            else:
                return QColor(182, 16, 0)
        except ValueError:
            return QColor(182, 16, 0)

    def check_count_of_ingred_bool(self, ind_ingr: str) -> bool:
        # check_count_of_ingred(), but returns bool
        try:
            ind_taken_el = self.ingredients_numbers.index(int(ind_ingr))
            if (int(self.ingredients_classes[ind_taken_el].get_count()) > 0):
                return True
            else:
                return False
        except ValueError:
            return False

    def check_count_of_ingred_in_recipe(self, all_ingreds: str) -> QColor:
        # check_count_of_ingred(), but used for recipe list
        res = list()
        for elem in str(all_ingreds).split():
            res.append(self.check_count_of_ingred_bool(elem))
        if (all(res)):
            return QColor(0, 158, 31)
        else:
            return QColor(182, 16, 0)

    def check_count_of_ingred_in_recipe_bool(self, all_ingreds: str) -> bool:
        # check_count_of_ingred(), but used for recipe list
        res = list()
        for elem in str(all_ingreds).split():
            res.append(self.check_count_of_ingred_bool(elem))
        if (all(res)):
            return True
        else:
            return False


# Dialog classes
class AddRecipeWindow(QDialog):
    # dialog class for adding recipes in DB
    def __init__(self):
        super().__init__()
        uic.loadUi('helpingElements/uiFolder/dialog.ui', self)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Добавление рецепта')

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accepted(self) -> list:
        return [self.name.text(), self.ingred.toPlainText(),
                self.recipe.toPlainText(), self.photoname.text()]


class AddIngredientWindow(QDialog):
    # dialog class for adding ingredients in DB
    def __init__(self):
        super().__init__()
        uic.loadUi('helpingElements/uiFolder/dialog2.ui', self)
        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle('Добавление ингредиента')

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accepted(self) -> tuple:
        return (self.name.text(), self.id_inp.value(), self.count_inp.value())


class ChangeRecipeWindow(AddRecipeWindow):
    # dialog class, same as AddRecipeWindow class, but with fixed name
    # Needed for changing some part of recipe
    def __init__(self, name, ingr, descr, pict):
        super().__init__()
        self.name.setText(name)
        self.name.setReadOnly(True)
        self.ingred.setPlainText(str(ingr))
        self.recipe.setPlainText(descr)
        self.photoname.setText(pict)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Изменение рецепта')

    def accepted(self) -> tuple:
        return (self.name.text(), self.ingred.toPlainText(),
                self.recipe.toPlainText(), self.photoname.text())


class CheckAssuranceWindow(QDialog):
    # dialog class, that asks the assurance about some action
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Вы уверены?')
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Вы уверены, что хотите удалить этот элемент?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accepted(self) -> bool:
        return True

    def rejected(self) -> bool:
        return False


# Other classes (basically, just containers for values)
class Recipe:
    def __init__(self, name, ingredients, description, pict, check_ingreds):
        self.recipe_name = name
        self.recipe_ingredients = ingredients
        self.recipe_description = description
        self.recipe_pict = pict
        self.all_ingreds = check_ingreds

    def __str__(self) -> str:
        return self.recipe_name

    def __call__(self) -> tuple:
        return (
            self.recipe_name, self.recipe_ingredients, self.recipe_description,
            self.recipe_pict)

    def get_all_ingreds(self) -> str:
        return self.all_ingreds

    def get_recipe_ingred(self) -> str:
        return self.recipe_ingredients


class Ingredient:
    def __init__(self, idd, name, count):
        self.ingr_id = idd
        self.ingr_name = name
        self.ingr_count = count

    def __call__(self) -> tuple:
        return (self.ingr_id, self.ingr_name, self.ingr_count)

    def get_count(self) -> str:
        return self.ingr_count


# executing app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainAppWindow()
    window.show()
    sys.exit(app.exec_())

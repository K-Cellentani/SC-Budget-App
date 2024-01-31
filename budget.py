class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.amount = 0

  def __str__(self):
    header_stars = int((30 - len(self.name))/2)
    stars = "*" * header_stars
    lstars = "*" * (header_stars + 1)
    output = []
    for i in self.ledger:
      amount = i['amount']
      amount = float(amount)
      amount = "{:.2f}".format(amount)
      amount = str(amount).rjust(6)
      description = i['description']
      description = str(description).ljust(23)
      output.append(f'{description[:23]} {amount}')
      total = "{:.2f}".format(self.amount)
    if len(self.name) % 2 == 0:
      return f'{stars}{self.name}{stars}\n' + '\n'.join(output) + f'\nTotal: {total}'
    else:
      return f'{lstars}{self.name}{stars}\n' + '\n'.join(output) + f'\nTotal: {total}'
  
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.amount += amount
  
  def withdraw(self, amount, description=""):
    if self.check_funds(amount) == True:
      self.ledger.append({"amount": -amount, "description": description})
      self.amount -= amount
      return True
    else:
      return False
    
  def get_balance(self):
    return sum(item['amount'] for item in self.ledger)
  
  def check_funds(self, amount):
    return amount <= self.get_balance()

  def transfer(self, amount, category):
    if self.check_funds(amount):
      description = f"Transfer to {category.name}"
      self.withdraw(amount, description)
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False
  
  
def create_spend_chart(categories):
  category_names = [category.name for category in categories if category]
  num_categories = len(category_names)

  chart = 'Percentage spent by category\n'
  
  percentages = []
  withdrawals = []
  for category in categories:
    if category:
      withdrawal = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
      withdrawals.append(abs(withdrawal))
    total_withdrawals = sum(withdrawals)
  if total_withdrawals > 0:
    for i in withdrawals:
      percentage = i / total_withdrawals * 100
      percentages.append(percentage)


  bar_heights = []
  for i in percentages:
    bar_heights.append(int(i / 10))
  
  for i in range(100, -1, -10):
    chart += f"{i:3}| "
    for height in bar_heights:
      if height >= i // 10:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"

  chart += "    " + "-" * (3 * num_categories + 1) + "\n"
  
  max_names = 0 
  for i in category_names:
    if max_names <= len(i):
      max_names = len(i)

  for i in range(max_names):
    chart += "     "
    for name in category_names:
      if i < len(name):
        chart += name[i] + "  "
      else:
        chart += "   "
    if i < max_names - 1:
      chart += "\n"

  return chart
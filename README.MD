# MCF_ExampleModule

🚀 **Example Module for [MasterCryptoFarmBot](https://github.com/masterking32/MasterCryptoFarmBot)** 🚀

Welcome to the example module for the MasterCryptoFarmBot! This module serves as a simple of how to create a bot module for the MasterCryptoFarmBot. While it doesn't perform any useful functions, it provides a great starting point for your development.

# 🛠️ Development Instructions 🛠️

1. **Install the MasterCryptoFarmBot**: Follow the installation instructions provided in the main repository.
2. **Clone this repository**: Clone [MCF_ExampleModule](https://github.com/masterking32/MCF_ExampleModule) into the `modules` directory of the MasterCryptoFarmBot.
3. **Rename the directory**: Rename the cloned `MCF_ExampleModule` to your desired module name.
4. **Run the MasterCryptoFarmBot**: Start the MasterCryptoFarmBot and enable the module in the control panel.

## 🖥️ How to Run

There are two ways to run this module:

1. **Using MasterCryptoFarmBot**: Enable the module through the MasterCryptoFarmBot control panel.
2. **Running the module directly**:
   Ensure you are in the correct directory of the module by navigating to it with:

```bash
cd modules/MCF_ExampleModule
```

If you renamed the directory, replace `MCF_ExampleModule` with the new name, then use the following command to run the module directly:

```bash
python bot.py
```

## 📂 File Structure

- `bot.py`: The main file of the module. This file is required for the module to be run by the MasterCryptoFarmBot.
- `logo.png`: The logo of the module. This file is optional and can be removed.
- `bot_settings_types.json`: The settings configuration file for the module. This file will be loaded by the MasterCryptoFarmBot to create the settings for the module in the control panel. You can add your custom settings here and check the types and structure of the settings in the file to create your own.
- `bot_settings.json`: This file will be created by the MasterCryptoFarmBot after the user sets the settings in the control panel. This file will be used by the module to read the settings and apply them.
- `accounts.json`: This file will be created by the MasterCryptoFarmBot after the user sets the accounts for the module in the control panel (Not Pyrogram accounts, Web Query Accounts). This file will be used by the module to read the accounts and apply them.
- `bot.log`: This file will be created to save the logs of the module and display them in the control panel.
- `FarmBot/FarmBot.py`: This file is the main file of the module. You can create your own classes and functions in this file or import other files to use them in the module.
- `.disabled_module_accounts`: If you want to disable the module accounts feature, create this file in the module directory. The MasterCryptoFarmBot will not generate the `accounts.json` file if this file is present.

## 👟 Start Development

- First, open the `bot.py` file and edit the `tgAccount` parameters.

- Open the `FarmBot/FarmBot.py` file and start coding your module. You have WebQuery (TgWebInitData) ready, which is used to interact with any kind of BotApps. The `self.web_app_query` is the `TgWebInitData` of the WebApp.

- Have fun coding your module!

## 🏪 Add Your Bot to the Store

Once you have developed your module, you can add it to the MasterCryptoFarmBot store to allow other people to install your module from the `Install new bot module` section in the control panel.
To do this, you need to contact us on Telegram and provide the following information:

- Is your module free or paid?
- If it’s paid, how much does it cost?
- If your module is paid, please provide a TON address to receive payments.
- What is the name of your module?
- What is the description of your module?
- Do you have plans to update your module in the future?
- You need to have a GitHub repository (private/public) for your module.
- If your GitHub repository is private, you need to add the `@masterking32` user as a collaborator to access the repository.

## [Telegram Group](https://t.me/MasterCryptoFarmBotGroup) / [Telegram Channel](https://t.me/MasterCryptoFarmBot)

---

Developed by [MasterkinG32](https://github.com/masterking32) for the [MasterCryptoFarmBot](https://github.com/masterking32/MasterCryptoFarmBot)

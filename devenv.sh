#!/bin/sh

# zsh 默认自带
brew install zsh

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
pip install autojump
wget 'https://raw.githubusercontent.com/jiji879/Rasengan/master/zshrc' -O ~/.zshrc
sudo chsh -s $(which zsh)

# neovim
brew install neovim
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
wget 'https://raw.githubusercontent.com/jiji879/Rasengan/master/vimrc' -O ~/.config/nvim/init.vim
nvim -c PluginInstall -c q  -c q

# python
sudo pip install virtualenv

# python3
brew install python3

# php7 & php-fpm
brew install php70

# mysql
brew install mysql

# nginx
brew install nginx

# iterm2
wget 'https://iterm2.com/downloads/stable/latest' -O ~/Downloads/iterm2.zip
unzip !$
mv iTerm.app /Applications

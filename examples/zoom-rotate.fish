function zoom-rotate --description 'rotate zoom background image'
    set -l codepath ~/path-to-zoom-rotate-repo
    set -l virtualpath ~/.local/share/virtualenvs/your-virtual-env
    $virtualpath/bin/python $codepath/main.py rotate --config_file $codepath/config.ini
end

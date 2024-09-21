import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const Header: React.FC = () => {
    return (
        <header className='flex justify-between'>
            <h1 className='title'>RamEats</h1>
            <Avatar>
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>CN</AvatarFallback>
            </Avatar>
        </header>
    );
};

export default Header;
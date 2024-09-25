"use client"

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useRouter } from 'next/navigation';
import { supabase } from '../../lib/supabase';

const Header: React.FC = () => {
    const router = useRouter();

    const handleLogout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) console.error('Error logging out:', error.message);
        else {
            console.log('User logged out');
            router.replace('/');
        }
    };

    return (
        <header className='flex justify-between'>
            <h1 className='title'>RamEats</h1>
            <Avatar onClick={handleLogout}>
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>CN</AvatarFallback>
            </Avatar>
        </header>
    );
};

export default Header;
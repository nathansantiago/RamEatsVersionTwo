import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';

export default function DashboardLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (
        <div className='flex flex-col min-h-screen p-4'>
            <Header />
            <main className='flex-grow justify-center flex items-center'>
                {children}
            </main>
            <div className='justify-center flex items-center'><Footer /></div>
        </div>
    );
};
import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';

const HomePage: React.FC = () => {
    return (
        <div className='flex flex-col min-h-screen p-4'>
            <Header />
            <main className='flex-grow'>
            </main>
            <div className='justify-center flex items-center'><Footer /></div>
        </div>
    );
};

export default HomePage;
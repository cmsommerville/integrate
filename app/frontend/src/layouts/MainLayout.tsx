import Header from "../components/Header";
import Sidebar from "../components/Sidebar";

const MainLayout = (props: any) => {
  return (
    <div className="min-h-screen w-screen flex">
      <Sidebar />
      <main className="flex-1">
        <Header />
        <div className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 md:px-8">
            {props.children}
          </div>
        </div>
      </main>
    </div>
  );
};

export default MainLayout;

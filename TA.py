import os

class Node:
    def __init__(self, no_sku, nama_barang, harga_barang, jumlah_stok):
        self.no_sku = no_sku
        self.nama_barang = nama_barang
        self.harga_barang = harga_barang
        self.jumlah_stok = jumlah_stok
        self.left = None
        self.right = None
        
class Binarysearchtree:
    def __init__(self):
        self.root = None
    
    def insert(self,no_sku,nama_barang,harga_barang,jumlah_stok):
        new_node = Node(no_sku,nama_barang,harga_barang,jumlah_stok)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_cek(self.root,no_sku,nama_barang,harga_barang,jumlah_stok)
            
    def _insert_cek(self, node, no_sku, nama_barang, harga_barang, jumlah_stok):
        if no_sku == node.no_sku:
            print("No.SKU sudah ada")
            return
        elif no_sku < node.no_sku:
            if node.left is None:
                node.left = Node(no_sku,nama_barang,harga_barang,jumlah_stok)
            else:
                self._insert_cek(node.left, no_sku, nama_barang, harga_barang, jumlah_stok)
        else:
            if node.right is None:
                node.right = Node(no_sku,nama_barang,harga_barang,jumlah_stok)
            else:
                self._insert_cek(node.right, no_sku, nama_barang, harga_barang, jumlah_stok)
                
    def restock(self, no_sku, jumlah_barang):
        if self.root is None:
            print("Data stok barang kosong. Silakan input data stok barang terlebih dahulu.")
            return
        else:
            self._restock_cek(self.root, no_sku, jumlah_barang)
            
    def _restock_cek(self, node, no_sku, jumlah_barang):
        if node is None:
            print("No.SKU tidak ditemukan")
            return
        elif no_sku == node.no_sku:
            node.jumlah_stok += jumlah_barang
            print("Restok berhasil")
            return
        elif no_sku < node.no_sku:
            self._restock_cek(node.left, no_sku, jumlah_barang)
        else:
            self._restock_cek(node.right, no_sku, jumlah_barang)
            
    def search(self, no_sku):
        return self._search_cek(self.root, no_sku)

    def _search_cek(self, node, no_sku):
        if node is None or node.no_sku == no_sku:
            return node
        elif no_sku < node.no_sku:
            return self._search_cek(node.left, no_sku)
        else:
            return self._search_cek(node.right, no_sku)
    
class Transaksi:
    def __init__(self, nama_konsumen, no_sku_barang, jumlah_beli):
        self.nama_konsumen = nama_konsumen
        self.no_sku_barang = no_sku_barang
        self.jumlah_beli = jumlah_beli
        self.subtotal = 0
    
def input_data_stok_barang(bst):
    no_sku_barang = input("Masukkan No. SKU: ")
    nama_barang = input("Masukkan Nama Barang: ")
    harga_barang = float(input("Masukkan Harga Satuan: "))
    jumlah_stok = int(input("Masukkan Jumlah Stok: "))
    bst.insert(no_sku_barang, nama_barang, harga_barang, jumlah_stok)
    
def restock_barang(bst):
    no_sku_barang = input("Masukkan No. SKU: ")
    jumlah_barang = int(input("Masukkan Jumlah Barang: "))
    bst.restock(no_sku_barang, jumlah_barang)
    
def input_data_transaksi(transaksi_list, bst):
    nama_konsumen = input("Masukkan Nama Konsumen: ")
    no_sku_barang = input("Masukkan No. SKU Barang: ")
    jumlah_beli = int(input("Masukkan Jumlah Beli: "))
    
    node = bst.search(no_sku_barang)
    if node is None:
        print("No. SKU yang diinputkan belum terdaftar.")
        lanjutkan = input("Apakah ingin melanjutkan transaksi (Y/N)? ")
        if lanjutkan.lower() == 'y':
            input_data_transaksi(transaksi_list, bst)
        else:
            return
    elif node.jumlah_stok < jumlah_beli:
        print("Jumlah stok No. SKU yang Anda beli tidak mencukupi.")
        lanjutkan = input("Apakah ingin melanjutkan transaksi (Y/N)? ")
        if lanjutkan.lower() == 'y':
            input_data_transaksi(transaksi_list, bst)
        else:
            return
    else:
        transaksi = Transaksi(nama_konsumen, no_sku_barang, jumlah_beli)
        transaksi.subtotal = node.harga_barang * jumlah_beli
        transaksi_list.append(transaksi)
        node.jumlah_stok -= jumlah_beli
        print("Data Transaksi Konsumen Berhasil Diinputkan.")
        tambah_data = input("Apakah ingin menambahkan data pembelian untuk konsumen ini (Y/N)? ")
        if tambah_data.lower() == 'y':
            input_data_transaksi(transaksi_list, bst)
        else:
            return
        
def lihat_data_seluruh_transaksi(transaksi_list):
    if not transaksi_list:
        print("Tidak ada data transaksi konsumen.")
        return

    print("Data Seluruh Transaksi Konsumen:")
    for transaksi in transaksi_list:
        print(f"Nama Konsumen: {transaksi.nama_konsumen}")
        print(f"No. SKU Barang: {transaksi.no_sku_barang}")
        print(f"Jumlah Beli: {transaksi.jumlah_beli}")
        print(f"Subtotal: {transaksi.subtotal}")
        
def lihat_data_transaksi_berdasarkan_subtotal(transaksi_list):
    n = len(transaksi_list)
    for i in range(n - 1):
        max_index = i
        for j in range(i + 1, n):
            if transaksi_list[j].subtotal > transaksi_list[max_index].subtotal:
                max_index = j
        transaksi_list[i], transaksi_list[max_index] = transaksi_list[max_index], transaksi_list[i]
    print("Data Transaksi Konsumen (Berdasarkan Subtotal):")
    print("=============================================")
    for transaksi in transaksi_list:
        print(f"Nama Konsumen: {transaksi.nama_konsumen}")
        print(f"No. SKU Barang: {transaksi.no_sku_barang}")
        print(f"Jumlah Beli: {transaksi.jumlah_beli}")
        print(f"Subtotal: {transaksi.subtotal}")
        print("---------------------------------------------")
        
def main():
    bst = Binarysearchtree()
    transaksi_list = []
    os.system("cls")
    while True:
        print("=== MENU UTAMA ===")
        print("1. Kelola Stok Barang")
        print("2. Kelola Transaksi Konsumen")
        print("0. Exit Program")

        pilihan_menu_utama = int(input("Pilih menu: "))

        if pilihan_menu_utama == 1:
            while True:
                print("=== SUB MENU KELOLA STOK BARANG ===")
                print("1. Input Data Stok Barang")
                print("2. Restok Barang")
                print("0. Kembali ke MENU UTAMA")

                pilihan_submenu_stok_barang = int(input("Pilih submenu: "))

                if pilihan_submenu_stok_barang == 1:
                    input_data_stok_barang(bst)
                elif pilihan_submenu_stok_barang == 2:
                    restock_barang(bst)
                elif pilihan_submenu_stok_barang == 0:
                    break
                else:
                    print("Pilihan submenu tidak valid.")
        elif pilihan_menu_utama == 2:
            while True:
                print("=== SUB MENU KELOLA TRANSAKSI KONSUMEN ===")
                print("1. Input Data Transaksi Baru")
                print("2. Lihat Data Seluruh Transaksi Konsumen")
                print("3. Lihat Data Transaksi Berdasarkan Subtotal")
                print("0. Kembali ke MENU UTAMA")

                pilihan_submenu_transaksi = int(input("Pilih submenu: "))

                if pilihan_submenu_transaksi == 1:
                    input_data_transaksi(transaksi_list, bst)
                elif pilihan_submenu_transaksi == 2:
                    lihat_data_seluruh_transaksi(transaksi_list)
                elif pilihan_submenu_transaksi == 3:
                    lihat_data_transaksi_berdasarkan_subtotal(transaksi_list)
                elif pilihan_submenu_transaksi == 0:
                    break
                else:
                    print("Pilihan submenu tidak valid.")
        elif pilihan_menu_utama == 0:
            break
        else:
            print("Pilihan menu tidak valid.")


if __name__ == "__main__":
    main()
